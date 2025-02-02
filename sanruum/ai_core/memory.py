from datetime import datetime
from typing import List, Any, Optional


class AIMemory:
    def __init__(self) -> None:
        self.conversation_history: List = []
        self.last_intent: Optional[str] = None  # Track last recognized intent, can be None or str

    def store_message(self, sender: str, message: str) -> None:
        """Stores messages in memory for context awareness, with timestamp."""
        self.conversation_history.append({
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def get_last_messages(self, limit: int = 5) -> List:
        """Retrieves last few messages to maintain context."""
        return self.conversation_history[-limit:]

    def set_last_intent(self, intent: str) -> None:
        """Tracks the last detected user intent."""
        self.last_intent = intent

    def get_last_intent(self) -> Any:
        """Returns the last recognized intent."""
        return self.last_intent

    def reset_memory(self) -> None:
        """Clears the conversation history and resets last intent."""
        self.conversation_history.clear()
        self.last_intent = None
