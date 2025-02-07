# sanruum\faq_handler.py
import json
from typing import Optional

from fuzzywuzzy import process

from sanruum.constants import FAQ_FILE
from sanruum.utils.logger import logger


class FAQHandler:
    def __init__(self) -> None:
        self.local_faq = {
            "appointment": "To book an appointment, please visit our website."
        }

        try:
            with open(FAQ_FILE, "r", encoding="utf-8") as f:
                self.faq_data = json.load(f)
            logger.info("✅ FAQ Data Loaded Successfully!")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(
                f"❌ Failed to Load FAQ JSON: {e}. Using default FAQ data."
            )
            self.faq_data = {}
        except Exception as e:
            logger.error(f"❌ Unexpected error loading FAQ JSON: {e}")
            self.faq_data = {}

    def get_answer(self, user_input: str) -> Optional[str]:
        user_input = user_input.strip().lower()

        # Handle common greetings
        greetings = {"hello", "hi", "hey", "hola"}
        if user_input in greetings:
            return "Hello! How can I assist you today?"

        # Split input if "and" is present
        questions = [q.strip() for q in user_input.split("and") if q.strip()]
        logger.debug(f"🛠 Split questions: {questions}")

        answers = []

        for question in questions:
            logger.debug(f"🔎 Processing question: '{question}'")

            # Try to find the best match
            best_match, score = process.extractOne(
                question, self.faq_data.keys(), score_cutoff=85
            ) or (None, 0)

            if best_match and score >= 85:  # Ensure match is valid
                logger.debug(f"✅ Best match: '{best_match}' (Score: {score})")
                answer = self.faq_data[best_match]

                if "automation" in answer.lower():
                    answer += " Would you like to know more about how automation can help your business?"

                answers.append(answer)
            else:
                logger.debug(
                    f"❌ No suitable match found for: '{question}' (Score: {score})"
                )
                answers.append(
                    "I'm not sure about that. Would you like me to help you find more information?"
                )

        return (
            "\n".join(answers)
            if answers
            else "Sorry, I couldn't find an answer. Would you like to ask something else?"
        )
