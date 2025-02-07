import time
import traceback

from sanruum.ai_core.config import PERSONALITY_MODE, RESPONSES
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
        """Generates a response based on user input, optimized for efficiency."""
        try:
            start_time = time.perf_counter()
            user_input = user_input.strip().lower()
            logger.info(f"📝 User Input: {user_input}")

            if known_info := self.memory.find_relevant_knowledge(user_input):
                return known_info

            if (
                    faq_answer := self.faq.get_answer(user_input)
            ) and faq_answer != "I'm sorry, I couldn't find an answer.":
                self.memory.store_knowledge(user_input, faq_answer)
                return faq_answer

            ai_response = self.processor.process_input(user_input)
            if (
                    ai_response
                    and ai_response not in RESPONSES[PERSONALITY_MODE]["fallback"]
            ):
                self.memory.store_knowledge(user_input, ai_response)

            logger.debug(
                f"Response time: {time.perf_counter() - start_time:.4f}s"
            )
            return ai_response

        except Exception as e:
            logger.error(
                f"❌ Error processing response: {e}\n{traceback.format_exc()}"
            )
            return "I'm experiencing some issues at the moment. Please try again later!"
