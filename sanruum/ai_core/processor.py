import random
from typing import Any

from sanruum.ai_core.config import PERSONALITY_MODE, RESPONSES


class AIProcessor:
    def __init__(self, memory: Any) -> None:
        self.memory = memory

    def process_input(self, user_input: str) -> str:
        """Processes user input and determines AI response based on intent."""
        # Store the user's input for memory/context tracking
        self.memory.store_message("user", user_input)
        user_input = user_input.lower()

        personality = RESPONSES.get(PERSONALITY_MODE, RESPONSES["friendly"])

        # Greetings
        if any(word in user_input for word in ["hello", "hi", "hey"]):
            return random.choice(personality["greeting"])

        # Farewell
        elif any(word in user_input for word in ["bye", "goodbye", "see you"]):
            return random.choice(personality["farewell"])

        # Appointment booking
        elif "appointment" in user_input:
            return "Would you like to book an appointment? 📅 I can help with that!"

        # Example of context-based response:
        elif "price" in user_input and self.memory.get_last_intent() == "services":
            return "Our pricing depends on the service package you choose. Would you like more details?"

        # Fallback based on dynamic conversation context
        return self.generate_dynamic_response(user_input)

    def generate_dynamic_response(self, user_input: str) -> str:
        """Generates a more dynamic response based on conversation history."""
        last_messages = self.memory.get_last_messages()

        # If the last message was a question, AI can offer to continue the conversation
        if last_messages and "?" in last_messages[-1]["message"]:
            return "Interesting! Tell me more. 🤔"

        # You can make this logic more complex later, based on memory
        return random.choice([
            "I'm still learning! What else can I help with?",
            "That's a good question! Let me think...",
            "I'm here to help. Can you clarify a bit?"
        ])
