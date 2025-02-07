# sanruum\ai_core\memory.py
"""
memory.py - Handles the memory system for AI conversations.

This module tracks conversation history, user intents, and reminders to maintain context
across interactions. It also provides methods to manage memory efficiently.

Class:
- AIMemory: Represents the AI's memory, stores conversation history, reminders, and user intents.

Key Methods:
- store_message(role: str, message: str) -> None: Stores a message in memory, keeping the latest ones.
- get_last_message() -> Optional[str]: Retrieves the last message stored.
- get_last_intent() -> Optional[str]: Retrieves the last intent detected.
- set_last_intent(intent: str) -> None: Sets the last detected user intent.
- add_reminder(reminder: str) -> None: Adds a reminder for follow-up actions.
- get_reminders() -> List[str]: Retrieves all stored reminders.
- reset_memory() -> None: Clears the entire memory.
"""
import json
import os.path
from typing import List, Optional, Dict, Any

from sentence_transformers import SentenceTransformer

from sanruum.constants import MEMORY_FILE


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
        """Stores a message in memory, keeping the latest ones."""
        vector = self.embedder.encode(message)
        if "history" not in self.memory:
            self.memory["history"] = []

        self.memory.append({"role": role, "message": message, "vector": vector})

        self.memory["history"].append({"role": role, "message": message})

        # Keep only the latest messages up to memory_limit
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
                return {}
        return {}

    def save_memory(self) -> None:
        """Save AI memory to file. """
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4)

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

    def find_relevant_knowledge(self, query: str) -> Optional[str]:
        """Search for the most relevant stored knowledge."""
        for topic, info in self.memory.items():
            if isinstance(info, list) and topic in query.lower():
                return " ".join(info)  # Return all stored info on the topic
        return None

    def get_last_message(self) -> Optional[str]:
        """Return the last message in memory."""
        history = self.memory.get("history", [])
        if isinstance(history, list) and history and isinstance(history[-1], dict):
            return history[-1].get("message")
        return None

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
