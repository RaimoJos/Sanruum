# sanruum\ai_core\response.py
from __future__ import annotations

import time
import traceback

from sanruum.ai_core.config import PERSONALITY_MODE
from sanruum.ai_core.config import RESPONSES
from sanruum.ai_core.memory import AIMemory
from sanruum.ai_core.processor import AIProcessor
from sanruum.faq_handler import FAQHandler
from sanruum.utils.logger import logger


class AIResponse:
    def __init__(self) -> None:
        self.memory = AIMemory()
        self.processor = AIProcessor(self.memory)
        self.faq = FAQHandler()
        self.response_cache: dict[str, str] = {}  # Type annotation for the cache

    def get_response(self, user_input: str) -> str:
        """
        Generates a response based on user input, optimized for efficiency.
        """
        try:
            start_time = time.perf_counter()
            user_input = user_input.strip().lower()
            logger.info(f'📝 User Input: {user_input}')

            # Check cache first
            if user_input in self.response_cache:
                logger.debug('✅ Cached response found')
                return self.response_cache[user_input]

            # Check memory for relevant knowledge
            if known_info := self.memory.find_relevant_knowledge(user_input):
                return known_info

            # Check FAQ
            faq_answer = self.faq.get_answer(user_input)
            if faq_answer and faq_answer != "I'm sorry, I couldn't find an answer.":
                self.memory.store_knowledge(user_input, faq_answer)
                self.response_cache[user_input] = faq_answer  # Cache the response
                return faq_answer

            ai_response = self.processor.process_input(user_input)

            if (
                    ai_response
                    and ai_response not in RESPONSES[PERSONALITY_MODE]['fallback']
                    # Avoid redundant storage
                    and ai_response not in self.memory.get_all_knowledge()
            ):
                self.memory.store_knowledge(user_input, ai_response)
                self.response_cache[user_input] = ai_response  # Cache response

            logger.debug(
                f'⏱️ Response time: {(time.perf_counter() - start_time) * 1000:.2f}ms',
            )

            # Ensure response is always a string
            return (
                ai_response
                if ai_response
                else "Sorry, I couldn't process your request."
            )

        except Exception as e:
            logger.error(f'❌ Error processing response: {e}\n{traceback.format_exc()}')
            return "I'm experiencing some issues at the moment. Please try again later!"
