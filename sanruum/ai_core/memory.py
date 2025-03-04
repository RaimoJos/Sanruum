# sanruum/ai_core/memory.py
from __future__ import annotations

import json
import os.path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from sanruum.config.base import BaseConfig
from sanruum.utils.base.logger import logger

MEMORY_FILE = BaseConfig.MEMORY_FILE


class AIMemory:
    def __init__(self, memory_limit: int = 10) -> None:
        """
        Initializes the AI memory object.

        Parameters:
            memory_limit (int): The number of messages to store in memory.
        """
        self.memory_limit = memory_limit
        self.memory: dict[str, Any] = self.load_memory()
        self.last_intent: str | None = None
        self.reminders: list[str] = []

        try:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f'❌ Failed to load SentenceTransformer: {e}')
            self.embedder = None

    def store_message(self, role: str, message: str) -> None:
        """Store a message while keeping the latest ones."""
        if self.embedder:
            vector = self.embedder.encode(message).tolist()
        else:
            vector = []
        self.memory.setdefault('history', []).append(
            {'role': role, 'message': message, 'vector': vector},
        )
        self.memory['history'] = self.memory['history'][-self.memory_limit:]
        self.save_memory()

    @staticmethod
    def load_memory() -> dict[str, Any]:
        """Load AI memory from file."""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, encoding='utf-8') as f:
                    data = json.load(f)
                    return {'history': data.get('history', [])}
            except json.JSONDecodeError:
                logger.error('❌ Memory file corrupted, resetting memory')
        return {'history': []}

    def save_memory(self) -> None:
        """Save AI memory to file."""
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            logger.error(f'❌ Failed to save memory: {e}')

    def find_relevant_knowledge(self, query: str) -> str | None:
        """Find the most relevant stored knowledge based on similarity."""
        if not self.embedder:
            logger.error('No embedder available for computing query vector.')
            return None

        query_vector = self.embedder.encode(query).reshape(1, -1)

        best_match = None
        best_score = -1

        knowledge = self.get_all_knowledge()
        if not knowledge:
            logger.debug('No stored knowledge!')
            return None

        for topic, items in knowledge.items():
            for item in items:
                # Use cached embedding if available
                if isinstance(item, dict) and 'vector' in item:
                    candidate_text = item['data']
                    candidate_vector = np.array(item['vector']).reshape(1, -1)
                else:
                    candidate_text = item
                    candidate_vector = self.embedder.encode(
                        candidate_text,
                    ).reshape(1, -1)

                similarity = cosine_similarity(query_vector, candidate_vector)[0][0]
                logger.debug(
                    f"Comparing '{query}' to"
                    f" '{candidate_text}' → similarity: {similarity}",
                )

                if similarity > best_score:
                    best_match = candidate_text
                    best_score = similarity

        if best_match is None or best_score < 0.3:
            logger.debug(f'No relevant match found (best_score: {best_score:.4f}).')
            return None

        logger.debug(f'✅ Best match found: {best_match} (Score: {best_score:.4f})')
        return best_match

    def get_last_message(self) -> str | None:
        """Return the last message in history."""
        if self.memory['history']:
            last_message = self.memory['history'][-1].get('message')
            if isinstance(last_message, str):
                return last_message
        return None

    def store_knowledge(self, topic: str, data: str) -> None:
        """Store new information under a topic, caching its embedding."""
        if self.embedder:
            vector = self.embedder.encode(data).tolist()
        else:
            vector = []
        knowledge_item = {'data': data, 'vector': vector}
        self.memory.setdefault(topic.lower(), []).append(knowledge_item)
        self.save_memory()

    def retrieve_knowledge(self, topic: str) -> list[str] | None:
        """Retrieve stored knowledge about a topic."""
        data = self.memory.get(topic.lower(), None)
        if isinstance(data, list):
            return [
                item['data']
                if isinstance(item, dict) and 'data' in item
                else item for item in data
            ]
        return None

    def get_all_knowledge(self) -> dict[str, list[str]]:
        """Retrieve all stored knowledge except conversation history."""
        result = {}
        for k, v in self.memory.items():
            if k != 'history' and isinstance(v, list):
                result[k] = [
                    item['data'] if isinstance(
                        item, dict,
                    ) and 'data' in item else item for item in v
                ]
        return result

    def get_last_intent(self) -> str | None:
        """Returns the last recognized intent."""
        return self.last_intent

    def set_last_intent(self, intent: str) -> None:
        """Tracks the last detected user intent."""
        self.last_intent = intent

    def add_reminder(self, reminder: str) -> None:
        """Store a reminder for follow-up action."""
        self.reminders.append(reminder)

    def get_reminders(self) -> list[str]:
        """Returns all stored reminders."""
        return self.reminders

    def reset_memory(self) -> None:
        """Clears the memory, reminders, and last intent."""
        self.memory = {'history': []}
        self.reminders.clear()
        self.last_intent = None
        self.save_memory()
