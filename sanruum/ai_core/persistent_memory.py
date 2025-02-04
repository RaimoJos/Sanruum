import os
import pickle

from sanruum.ai_core.memory import AIMemory
from sanruum.constants import USER_MEMORY_DIR


class PersistentAIMemory(AIMemory):
    def __init__(self, user_id: str) -> None:
        super().__init__()
        self.user_id = user_id
        self.load_user_memory()

    def load_user_memory(self) -> None:
        """Load memory from a file or database for the specific user."""
        try:
            file_path: str = os.path.join(USER_MEMORY_DIR, f"memory_{self.user_id}.pkl")
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    self.conversation_history = pickle.load(file)
                    self.last_intent = pickle.load(file)
        except FileNotFoundError:
            self.conversation_history = []
            self.last_intent = None

    def store_message(self, sender: str, message: str) -> None:
        super().store_message(sender, message)
        self.persist_memory()

    def persist_memory(self) -> None:
        """Persist the conversation history and last intent."""
        with open(f"memory_{self.user_id}.pkl", "wb") as file:
            pickle.dump(self.conversation_history, file)
            pickle.dump(self.last_intent, file)
