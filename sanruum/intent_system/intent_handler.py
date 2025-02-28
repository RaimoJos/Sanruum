from __future__ import annotations

import json
import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from sanruum.config import BaseConfig
from sanruum.utils.base.base_tools import get_current_time
from sanruum.utils.base.logger import logger

INTENTS_FILE = BaseConfig.INTENTS_FILE

DYNAMIC_INTENTS = {
    'time': get_current_time,
    # Add more dynamic intents here
}


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

    def get_intent_response(
            self, user_input: str,
    ) -> dict[str, str] | str:
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

                    intent_name = intent.get('name')

                    # Handle dynamic intents
                    if intent_name in DYNAMIC_INTENTS:
                        dynamic_value = DYNAMIC_INTENTS[intent_name]()  # Call function
                        response_templates = intent.get('response', {})

                        if isinstance(response_templates, dict):
                            chosen_response: str = response_templates.get(
                                'friendly', response_templates.get(
                                    list(response_templates.keys())[0],
                                    self.default_responses['fallback'],
                                ),
                            )
                            return chosen_response.format(time=dynamic_value)

                        if isinstance(response_templates, str):
                            return response_templates.format(time=dynamic_value)

                    # Return normal static response
                    response = intent.get('response')
                    if isinstance(response, (str, dict)):
                        return response

        logger.debug('❌ No matching intent found.')
        return self.default_responses['fallback']
