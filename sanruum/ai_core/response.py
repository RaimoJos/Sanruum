import random
import traceback
from typing import Optional

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
        """Generates a response based on user input using FAQ, AIProcessor, and fallback handling."""
        try:
            user_input = user_input.strip().lower()  # Normalize input
            logger.info(f"📝 User Input Received: {user_input}")

            # ✅ Check if FAQ has an answer
            faq_answer: Optional[str] = self.faq.get_answer(user_input)
            if faq_answer and faq_answer != "I'm sorry, I couldn't find an answer.":
                logger.debug(f"📚 FAQ Matched: {faq_answer}")
                self.memory.store_message("ai", faq_answer)
                return faq_answer

            # ✅ Process AI logic if FAQ did not match
            ai_response: Optional[str] = self.processor.process_input(user_input)
            if ai_response is not None:
                logger.info(f"🤖 AI Response Generated: {ai_response}")
                self.memory.store_message("ai", ai_response)
                return ai_response

            # ✅ Use a fallback response if nothing else works
            fallback_response: str = random.choice(
                RESPONSES.get(PERSONALITY_MODE, {}).get("fallback", ["I don't know."]))
            logger.warning(f"⚠️ Fallback Response Used: {fallback_response}")
            return fallback_response

        except Exception as e:
            logger.error(f"❌ Error processing response: {e}\n{traceback.format_exc()}")
            return "I'm experiencing some issues at the moment. Please try again later!"
