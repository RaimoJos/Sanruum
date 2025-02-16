# sanruum\faq_handler.py
from __future__ import annotations

import json

from fuzzywuzzy import process

from sanruum.constants import FAQ_FILE
from sanruum.utils.logger import logger


class FAQHandler:
    def __init__(self) -> None:
        self.local_faq = {
            'appointment': 'To book an appointment, please visit our website.',
        }

        try:
            with open(FAQ_FILE, encoding='utf-8') as f:
                self.faq_data = json.load(f)
            logger.info('✅ FAQ Data Loaded Successfully!')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(
                f'❌ Failed to Load FAQ JSON: {e}. Using default FAQ data.',
            )
            self.faq_data = {}
        except Exception as e:
            logger.error(f'❌ Unexpected error loading FAQ JSON: {e}')
            self.faq_data = {}

    def get_answer(self, user_input: str) -> str | None:
        user_input = user_input.strip().lower()
        questions = [q.strip() for q in user_input.split('and') if q.strip()]
        logger.debug(f'🛠 Split questions: {questions}')

        all_faqs = {**self.local_faq, **self.faq_data}  # Ensure merged dictionary
        logger.debug(f'📖 Available FAQ keys: {list(all_faqs.keys())}')  # Debugging

        answers = []
        for question in questions:
            logger.debug(f"🔎 Processing question: '{question}'")

            best_match, score = process.extractOne(
                question, all_faqs.keys(), score_cutoff=65,
            ) or (None, 0)

            if best_match:
                logger.debug(f"✅ Best match: '{best_match}' (Score: {score})")
                answer = all_faqs[best_match]
                answers.append(answer)
            else:
                logger.debug(
                    f"❌ No suitable match found for: '{question}' (Score: {score})",
                )
                answers.append(
                    "I'm not sure about that. Would you like me to "
                    'help you find more information?',
                )

        return '\n'.join(
            answers,
        ) if answers else (
            "Sorry, I couldn't find an answer. Would you like "
            'to ask something else?'
        )
