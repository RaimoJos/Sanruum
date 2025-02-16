# sanruum\ai_core\persistent_memory.py
from __future__ import annotations

import os
import pickle

from sanruum.ai_core.memory import AIMemory
from sanruum.constants import USER_MEMORY_DIR
from sanruum.utils.logger import logger


class PersistentAIMemory(AIMemory):
    def __init__(self, user_id: str) -> None:
        """Initialize PersistentAIMemory for a specific user."""
        super().__init__()
        self.user_id = user_id
        self.memory_file = os.path.join(USER_MEMORY_DIR, f'memory_{self.user_id}.pkl')
        self.load_user_memory()

    def load_user_memory(self) -> None:
        """Load memory from a file for the specific user."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as file:
                    self.memory, self.last_intent = pickle.load(file)
                    if not isinstance(self.memory, dict):
                        self.memory = {'history': []}  # Ensure it's a dictionary
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            self.memory = {'history': []}  # Default to empty history
            self.last_intent = None
            logger.error(f'❌ Failed to load user memory for {self.user_id}: {e}')

    def store_message(self, role: str, message: str) -> None:
        """Store a message while keeping the latest ones."""
        vector = self.embedder.encode(message).tolist() if self.embedder else []

        self.memory.setdefault('history', []).append(
            {'role': role, 'message': message, 'vector': vector},
        )

        # Keep only the latest messages
        self.memory['history'] = self.memory['history'][-self.memory_limit:]
        self.persist_memory()

    def persist_memory(self) -> None:
        """Persist the AI's memory and last detected intent to a file."""
        os.makedirs(USER_MEMORY_DIR, exist_ok=True)  # Ensure directory exists
        try:
            with open(self.memory_file, 'wb+') as file:
                pickle.dump((self.memory, self.last_intent), file)
        except Exception as e:
            logger.error(f'❌ Failed to persist memory for user {self.user_id}: {e}')

    def reset_memory(self) -> None:
        """Clears all memory, including persistent storage."""
        super().reset_memory()
        self.memory = {'history': []}  # Default to empty history
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        logger.info(f'✅ Memory reset for user {self.user_id}.')
