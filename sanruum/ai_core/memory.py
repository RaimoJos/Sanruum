# sanruum\ai_core\memory.py
import json
import os.path
from typing import Any, Dict, List, Optional

from sentence_transformers import SentenceTransformer

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
        self.memory: Dict[str, Any] = self.load_memory()
        self.last_intent: Optional[str] = None
        self.reminders: List[str] = []
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def store_message(self, role: str, message: str) -> None:
        """Store a message while keeping the latest ones."""
        vector = self.embedder.encode(message)

        if "history" not in self.memory:
            self.memory["history"] = []

        self.memory["history"].append(
            {"role": role, "message": message, "vector": vector}
        )

        # Keep only the latest messages
        self.memory["history"] = self.memory["history"][-self.memory_limit:]
        self.save_memory()

    @staticmethod
    def load_memory() -> Dict[str, List[str]]:
        """Load AI memory from file."""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error("❌ Memory file corrupted, resetting memory")
                return {"history": []}
        return {"history": []}

    def save_memory(self) -> None:
        """Save AI memory to file."""
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            logger.error(f"❌ Failed to save memory: {e}")

    def find_relevant_knowledge(self, query: str) -> Optional[str]:
        """Find the most relevant stored knowledge based on similarity."""
        query_vector = self.embedder.encode(query)
        best_match = None
        best_score = -1

        for topic, info in self.memory.items():
            if isinstance(info, list):
                for item in info:
                    item_vector = self.embedder.encode(item)
                    similarity = (
                            query_vector @ item_vector
                    )  # Dot product for similarity
                    if similarity > best_score:
                        best_match = item
                        best_score = similarity

        return best_match

    def get_last_message(self) -> Optional[str]:
        """Return the last message in history."""
        if self.memory["history"]:
            return self.memory["history"][-1].get("message")
        return None

    def store_knowledge(self, topic: str, data: str) -> None:
        """Store new information under a topic."""
        topic = topic.lower()
        if topic not in self.memory:
            self.memory[topic] = []
        if data not in self.memory[topic]:
            self.memory[topic].append(data)
        self.save_memory()

    def retrieve_knowledge(self, topic: str) -> Optional[List[str]]:
        """Retrieve stored knowledge about a topic."""
        return self.memory.get(topic.lower(), None)

    def get_last_intent(self) -> Optional[str]:
        """Returns the last recognized intent."""
        return self.last_intent

    def set_last_intent(self, intent: str) -> None:
        """Tracks the last detected user intent."""
        self.last_intent = intent

    def add_reminder(self, reminder: str) -> None:
        """Store a reminder for follow-up action."""
        self.reminders.append(reminder)

    def get_reminders(self) -> List[str]:
        """Returns all stored reminders."""
        return self.reminders

    def reset_memory(self) -> None:
        """Clears the memory, reminders, and last intent."""
        self.memory.clear()
        self.memory["history"] = []  # Ensure history remains a list
        self.reminders.clear()
        self.last_intent = None
        self.save_memory()
