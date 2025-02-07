# sanruum\ai_core\persistent_memory.py
"""
persistent_memory.py - Handles persistent memory storage for individual users.

This module extends the AIMemory class to provide functionality for persisting
conversation history and user intents to disk. It allows for loading and saving memory
for each user.

Class:
- PersistentAIMemory: Inherits from AIMemory and allows for persistent storage and retrieval.

Key Methods:
- load_user_memory() -> None: Loads user-specific memory from the file system.
- store_message(sender: str, message: str) -> None: Stores a message in memory and persists it.
- persist_memory() -> None: Persists the current memory to disk.
"""

import os
import pickle

from sanruum.ai_core.memory import AIMemory
from sanruum.constants import USER_MEMORY_DIR
from sanruum.utils.logger import logger


class PersistentAIMemory(AIMemory):
    def __init__(self, user_id: str) -> None:
        """
        Initialize PersistentAIMemory for a specific user."""
        super().__init__()
        self.user_id = user_id
        self.memory_file = os.path.join(
            USER_MEMORY_DIR, f"memory_{self.user_id}.pkl"
        )
        self.load_user_memory()

    def load_user_memory(self) -> None:
        """Load memory from a file for the specific user."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "rb") as file:
                    self.memory = self.last_intent = pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            self.memory = []  # Reset memory on failure
            self.last_intent = None
            logger.error(
                f"❌ Failed to load user memory for {self.user_id}: {e}"
            )

    def store_message(self, sender: str, message: str) -> None:
        """Store the user's message and persist memory."""
        super().store_message(sender, message)
        self.persist_memory()

    def persist_memory(self) -> None:
        """Persist the AI's memory and last detected intent to a file."""
        os.makedirs(USER_MEMORY_DIR, exist_ok=True)  # Ensure directory exists
        try:
            with open(self.memory_file, "wb+") as file:
                pickle.dump((self.memory, self.last_intent), file)
        except Exception as e:
            logger.error(
                f"❌ Failed to persist memory for user {self.user_id}: {e}"
            )

    def reset_memory(self) -> None:
        """Clears all memory, including persistent storage."""
        super().reset_memory()
        self.memory = []
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        logger.info(f"✅ Memory reset for user {self.user_id}.")
