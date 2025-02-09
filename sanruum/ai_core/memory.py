from __future__ import annotations

import json
import os.path
from typing import Any

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from sanruum.constants import MEMORY_FILE
from sanruum.utils.logger import logger


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

        query_vector = self.embedder.encode(query).reshape(1, -1)  # Reshape for sklearn
        logger.debug(f'Query Vector: {query_vector}')

        best_match = None
        best_score = -1

        knowledge = self.get_all_knowledge()
        if not knowledge:
            logger.debug('No stored knowledge!')
            return None

        for topic, info in knowledge.items():
            for item in info:
                item_vector = self.embedder.encode(item).reshape(1, -1)
                similarity = cosine_similarity(query_vector, item_vector)[0][0]
                logger.debug(
                    f"Comparing '{query}' to '{item}' → similarity: {similarity}",
                )

                if similarity > best_score:
                    best_match = item
                    best_score = similarity

        if best_match is None:
            logger.debug('No match found!')

        return best_match

    def get_last_message(self) -> str | None:
        """Return the last message in history."""
        if self.memory['history']:
            last_message = self.memory['history'][-1].get('message')
            if isinstance(last_message, str):  # Ensure it's a string
                return last_message
        return None

    def store_knowledge(self, topic: str, data: str) -> None:
        """Store new information under a topic."""
        self.memory.setdefault(topic.lower(), []).append(data)
        self.save_memory()

    def retrieve_knowledge(self, topic: str) -> list[str] | None:
        """Retrieve stored knowledge about a topic."""
        data = self.memory.get(topic.lower(), None)
        if isinstance(data, list):
            return data
        return None

    def get_all_knowledge(self) -> dict[str, list[str]]:
        """Retrieve all stored knowledge except conversation history."""
        return {
            k: v for k, v in self.memory.items()
            if k != 'history' and isinstance(v, list)
        }

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
