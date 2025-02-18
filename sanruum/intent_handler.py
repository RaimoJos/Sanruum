from __future__ import annotations

import json
import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from sanruum.constants import INTENTS_FILE
from sanruum.utils.logger import logger


def remove_initial_greeting(text: str) -> str:
    greetings = {'hello', 'hi', 'hey'}
    words = text.split()
    if words and words[0] in greetings:
        return ' '.join(words[1:])
    return text


class IntentHandler:
    def __init__(self) -> None:
        self.default_responses = {
            'fallback': "I'm not sure about that."
                        ' Would you like me to help you find more information?',
        }

        try:
            with open(INTENTS_FILE, encoding='utf-8') as f:
                self.intents_data = json.load(f).get('intents', [])
            logger.info('✅ Intents Data Loaded Successfully!')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(
                f'❌ Failed to Load Intents JSON: {e}. Using default responses.',
            )
            self.intents_data = []
        except Exception as e:
            logger.error(f'❌ Unexpected error loading Intents JSON: {e}')
            self.intents_data = []

    def get_intent_response(self, user_input: str) -> str:
        user_input = user_input.strip().lower()
        user_input = remove_initial_greeting(user_input)
        questions = [q.strip() for q in re.split(r'[,.?!]', user_input) if q.strip()]
        logger.debug(f'🛠 Split questions: {questions}')

        for question in questions:
            logger.debug(f"🔎 Processing question: '{question}'")
            for intent in self.intents_data:
                best_match, score = process.extractOne(
                    question, intent.get('patterns', []),
                    scorer=fuzz.token_set_ratio, score_cutoff=60,
                ) or (None, 0)
                if best_match:
                    logger.debug(
                        f'✅ Best match found in intent: '
                        f"'{intent['name']}' (Score: {score})",
                    )
                    return str(
                        intent.get(
                            'response',
                            self.default_responses['fallback'],
                        ),
                    )

        logger.debug('❌ No matching intent found.')
        return str(self.default_responses['fallback'])  # Ensure it's a string.
