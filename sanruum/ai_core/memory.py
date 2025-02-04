from typing import List, Optional, Dict


class AIMemory:
    def __init__(self) -> None:
        self.conversation_history: List[str] = []
        self.last_intent: Optional[str] = None
        self.reminders: List[str] = []
        self.memory: List[Dict[str, str]] = []

    def store_message(self, role: str, message: str) -> None:
        self.memory.append({"role": role, "message": message})
        if len(self.memory) > 10:  # Keep recent 10 messages
            self.memory.pop(0)

    def get_last_message(self) -> Optional[str]:
        return self.memory[-1].get("message", "") if self.memory else None

    def get_last_intent(self) -> Optional[str]:
        """Returns the last recognized intent."""
        return self.last_intent  # ✅ Correct type hint

    def set_last_intent(self, intent: str) -> None:
        """Tracks the last detected user intent."""
        self.last_intent = intent

    def add_reminder(self, reminder: str) -> None:
        """Store a reminder for follow-up action."""
        self.reminders.append(reminder)

    def get_reminders(self) -> List:
        """Returns all stored reminders."""
        return self.reminders

    def reset_memory(self) -> None:
        """Clears the conversation history and resets last intent."""
        self.conversation_history.clear()
        self.last_intent = None
