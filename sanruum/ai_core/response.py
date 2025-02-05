import random
import traceback

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
        """Generates a response based on user input, including learning from new data."""
        try:
            user_input = user_input.strip().lower()
            logger.info(f"📝 User Input: {user_input}")

            # 1️⃣ Memory Lookup
            if (known_info := self.memory.find_relevant_knowledge(user_input)):
                logger.info(f"📖 Retrieved from Memory: {known_info}")
                return known_info

            # 2️⃣ FAQ System Check
            if (
                    faq_answer := self.faq.get_answer(
                        user_input)) and faq_answer != "I'm sorry, I couldn't find an answer.":
                self.memory.store_knowledge(user_input, faq_answer)
                return faq_answer

            # 3️⃣ Process AI Logic
            if (ai_response := self.processor.process_input(user_input)):
                self.memory.store_knowledge(user_input, ai_response)
                return ai_response

            # 4️⃣ Fallback Response
            fallback_response = random.choice(
                RESPONSES.get(PERSONALITY_MODE, {}).get("fallback", ["I don't know."])
            )
            self.memory.store_knowledge(user_input, fallback_response)
            return fallback_response

        except Exception as e:
            logger.error(f"❌ Error processing response: {e}\n{traceback.format_exc()}")
            return "I'm experiencing some issues at the moment. Please try again later!"
