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
    memory: AIMemory
    processor: AIProcessor
    faq: FAQHandler
    response_cache: dict[str, str]

    def __init__(self) -> None:
        self.memory = AIMemory()
        self.processor = AIProcessor(self.memory)
        self.faq = FAQHandler()
        # Initialize cache as an empty dictionary (consider cache eviction if needed)
        self.response_cache = {}

    def get_response(self, user_input: str | list) -> str:
        try:
            start_time = time.perf_counter()

            # Ensure input is a string
            if isinstance(user_input, list):
                user_input = ' '.join(map(str, user_input))
            if not isinstance(user_input, str):
                raise ValueError(
                    f'Invalid input type: {type(user_input)}. Expected string or list.',
                )

            user_input = user_input.strip().lower()
            logger.info(f'📝 User Input: {user_input}')

            # Check cache first
            if user_input in self.response_cache:
                cached_response = self.response_cache[user_input]
                logger.debug(f'✅ Cached response found: {cached_response}')
                return cached_response

            # Check memory for relevant knowledge
            if known_info := self.memory.find_relevant_knowledge(user_input):
                logger.debug(f'📚 Memory response found: {known_info}')
                self.response_cache[user_input] = known_info
                return known_info

            # Check FAQ
            faq_answer = self.faq.get_answer(user_input)
            default_faq_no_answer = "I'm sorry, I couldn't find an answer."
            logger.debug(f"FAQ answer returned for '{user_input}': {faq_answer}")
            if (
                    faq_answer and faq_answer.strip()
                    and faq_answer != default_faq_no_answer
            ):
                logger.debug(f'🔍 FAQ response found: {faq_answer}')
                self.memory.store_knowledge(user_input, faq_answer)
                self.response_cache[user_input] = faq_answer
                return faq_answer

            # If FAQ returns a falsey value, return a fallback message
            if not faq_answer or not faq_answer.strip():
                logger.debug(
                    '❌ No FAQ match found, skipping memory storage for this query.',
                )
                return (
                    "I'm not sure about that. Would you like me "
                    'to help you find more information?'
                )

            # If FAQ wasn't helpful, process via AI Processor
            ai_response = self.processor.process_input(user_input)

            # Store response if valid and not redundant
            if (
                    ai_response and ai_response
                    not in RESPONSES[PERSONALITY_MODE]['fallback']
            ):
                if not self.memory.find_relevant_knowledge(ai_response):
                    self.memory.store_knowledge(user_input, ai_response)
                    self.response_cache[user_input] = ai_response

            logger.debug(
                f'⏱️ Response time: {(time.perf_counter() - start_time) * 1000:.2f}ms',
            )
            final_response = ai_response or "Sorry, I couldn't process your request."
            logger.debug(f'🤖 Final AI response: {final_response}')
            return final_response
        except Exception as e:
            logger.error(f'❌ Error processing response: {e}\n{traceback.format_exc()}')
            return "I'm experiencing some issues at the moment. Please try again later!"
