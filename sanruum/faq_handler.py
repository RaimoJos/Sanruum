import json
from typing import Optional

from fuzzywuzzy import process

from sanruum.constants import FAQ_FILE
from sanruum.utils.logger import logger


class FAQHandler:
    def __init__(self) -> None:
        try:
            with open(FAQ_FILE, "r", encoding="utf-8") as f:
                self.faq_data = json.load(f)
            logger.info("✅ FAQ Data Loaded Successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to Load FAQ JSON: {e}")
            self.faq_data = {}

    def get_answer(self, user_input: str) -> Optional[str]:
        user_input = user_input.strip().lower()  # Normalize input

        # Check for common greetings
        greetings = ["hello", "hi", "hey", "hola"]
        if any(greeting in user_input for greeting in greetings):
            return "Hello! How can I assist you today?"

        # Split input into multiple parts based on "and" (if present)
        questions = [q.strip() for q in user_input.split("and") if q.strip()]
        if not questions:
            questions = [user_input]  # fallback to the whole input if splitting fails

        logger.debug(f"Split questions: {questions}")

        answers = []

        for question in questions:
            logger.debug(f"Processing question: '{question}'")
            best_match, score = process.extractOne(question, self.faq_data.keys())
            logger.debug(f"Best match found: '{best_match}' with score: {score}")

            if score >= 75:
                answer = self.faq_data[best_match]
                if "automation" in answer.lower():
                    answer += " Would you like to know more about how automation can help your business?"
                answers.append(answer)
            else:
                # Special handling: if the question mentions 'automation'
                if "automation" in question:
                    # Look for any FAQ answer containing the word "automation"
                    found = False
                    for key, ans in self.faq_data.items():
                        if "automation" in ans.lower():
                            answer = ans
                            if "automation" in answer.lower():
                                answer += " Would you like to know more about how automation can help your business?"
                            answers.append(answer)
                            found = True
                            break
                    if not found:
                        answers.append("Sorry, I didn't understand that. Could you please clarify your question?")
                else:
                    answers.append("Sorry, I didn't understand that. Could you please clarify your question?")

        # Combine multiple answers with line breaks if necessary
        if len(answers) > 1:
            return "\n".join(answers)
        return answers[0]
