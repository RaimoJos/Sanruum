import random

from sanruum.ai_core.config import RESPONSES, PERSONALITY_MODE
from sanruum.ai_core.memory import AIMemory
from sanruum.ai_core.processor import AIProcessor
from sanruum.faq_handler import FAQHandler
from sanruum.utils.logger import logger


class AIResponse:
    def __init__(self) -> None:
        self.memory = AIMemory()
        self.processor = AIProcessor(self.memory)
        self.faq = FAQHandler()

    def get_response(self, user_input: str) -> str:
        user_input = user_input.strip().lower()  # Normalize input

        # Check if FAQ matches
        faq_answer = self.faq.get_answer(user_input)
        if faq_answer:
            logger.debug(f"FAQ Answer Found: {faq_answer}")
            self.memory.store_message("ai", faq_answer)  # Store FAQ answer for context
            return faq_answer

        # ✅ Check if AIProcessor generates a valid response
        ai_response = self.processor.process_input(user_input)
        if ai_response:
            logger.info(f"🤖 AI Processor Output: {ai_response}")
            self.memory.store_message("ai", ai_response)  # Store AI response for context
            return ai_response

        # ✅ Use fallback if nothing else works
        fallback_response = random.choice(RESPONSES[PERSONALITY_MODE]["fallback"])
        logger.info(f"⚠️ Using Fallback Response: {fallback_response}")
        return fallback_response
