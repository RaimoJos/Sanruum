from __future__ import annotations

import time
import traceback

from sanruum.ai_core.ai_config import INTENTS
from sanruum.ai_core.memory import AIMemory
from sanruum.ai_core.processor import AIProcessor
from sanruum.config import BaseConfig
from sanruum.intent_system.intent_handler import IntentHandler
from sanruum.utils.base.logger import logger

PERSONALITY_MODE = BaseConfig.PERSONALITY_MODE


def apply_personality(response: str, personality: str) -> str:
    """
    Optionally fine-tunes the already personality-specific response.
    """
    if personality == 'friendly' and '😊' not in response:
        response = response.strip() + ' 😊'
    elif personality == 'formal':
        response = response.strip()
        if response and not response[0].isupper():
            response = response[0].upper() + response[1:]
    elif personality == 'professional':
        response = ' '.join(response.split())
    elif personality == 'casual' and not response.endswith('!'):
        response = response.strip() + '!'
    elif personality == 'humorous' and 'lol' not in response.lower():
        response = response.strip() + ' lol'

    return response


class AIResponse:
    personality: str
    memory: AIMemory
    processor: AIProcessor
    intent_handler: IntentHandler
    response_cache: dict[str, str]

    def __init__(self, personality: str = PERSONALITY_MODE) -> None:
        self.personality = personality
        self.memory = AIMemory()
        self.processor = AIProcessor(self.memory)
        self.intent_handler = IntentHandler()
        self.response_cache = {}

    def get_response(self, user_input: str | list) -> str:
        try:
            start_time = time.perf_counter()

            if isinstance(user_input, list):
                user_input = ' '.join(map(str, user_input))
            if not isinstance(user_input, str):
                raise ValueError(
                    f'Invalid input type: {type(user_input)}. Expected string or list.',
                )

            user_input = user_input.strip().lower()
            logger.info(f'📝 User Input: {user_input}')

            if user_input in self.response_cache:
                cached_response = self.response_cache[user_input]
                logger.debug(f'✅ Cached response found: {cached_response}')
                return cached_response

            if known_info := self.memory.find_relevant_knowledge(user_input):
                logger.debug(f'📚 Memory response found: {known_info}')
                self.response_cache[user_input] = known_info
                return known_info

            # Check Intents instead
            intent_response = self.intent_handler.get_intent_response(user_input)
            if intent_response:
                logger.debug(f'🔍 Intent response found: {intent_response}')
                if isinstance(intent_response, dict):
                    selected = intent_response.get(PERSONALITY_MODE)
                    if not selected:
                        selected = next(iter(intent_response.values()))
                    logger.debug(f'Selected personality response: {selected}')
                    intent_response = selected

                self.memory.store_knowledge(user_input, intent_response)
                self.response_cache[user_input] = intent_response
                return intent_response

            ai_response = self.processor.process_input(user_input)
            # If the processor returns a dict, select the personality-specific string.
            if isinstance(ai_response, dict):
                selected = ai_response.get(PERSONALITY_MODE)
                if not selected:
                    selected = next(iter(ai_response.values()))
                logger.debug(f'Selected processor response: {selected}')
                ai_response = selected

            fallbacks = INTENTS.get(PERSONALITY_MODE, {}).get('fallback', [])
            if ai_response and ai_response not in fallbacks:
                if not self.memory.find_relevant_knowledge(ai_response):
                    self.memory.store_knowledge(user_input, ai_response)
                    self.response_cache[user_input] = ai_response

            logger.debug(
                f'⏱️ Response time: {(time.perf_counter() - start_time) * 1000:.2f}ms',
            )
            final_response = ai_response or "Sorry, I couldn't process your request."
            final_response = apply_personality(final_response, self.personality)
            logger.debug(
                f'🤖 Final AI response (after personality applied): {final_response}',
            )
            return final_response
        except Exception as e:
            logger.error(f'❌ Error processing response: {e}\n{traceback.format_exc()}')
            return "I'm experiencing some issues at the moment. Please try again later!"
