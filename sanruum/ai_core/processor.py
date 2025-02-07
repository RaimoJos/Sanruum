import random
import time

import spacy
import torch
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sanruum.ai_core.config import PERSONALITY_MODE, RESPONSES
from sanruum.ai_core.memory import AIMemory
from sanruum.utils.logger import logger

# Initialize Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Load AI Models
analyzer = SentimentIntensityAnalyzer()
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0 if device.type == "cuda" else -1,
)

try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.error(f"Failed to load Spacy NLP model: {e}")
    nlp = None


class AIProcessor:
    def __init__(self, memory: AIMemory) -> None:
        self.memory = memory
        self.context = []

    def process_input(self, user_input: str) -> str:
        """Processes user input and determines AI response."""
        start_time = time.perf_counter()
        user_input = user_input.strip().lower()
        self.memory.store_message("user", user_input)

        # Check stored knowledge & reminders first
        if knowledge_response := self.memory.find_relevant_knowledge(
                user_input
        ):
            return knowledge_response
        if reminders := self.memory.get_reminders():
            return f"Reminder: {reminders[0]}"

        sentiment = self.analyze_sentiment(user_input)
        intents = self.extract_intents(user_input)

        intent_responses = {
            "greeting": RESPONSES[PERSONALITY_MODE].get(
                "greeting", ["Hello!"]
            ),
            "farewell": RESPONSES[PERSONALITY_MODE].get(
                "farewell", ["Goodbye!"]
            ),
            "appointment": ["Would you like to book an appointment? 📅"],
            "pricing": [
                "Our pricing depends on the service package you choose. Would you like more details?"
            ],
            "services": [
                "We offer various AI-powered services. Need specifics?"
            ],
        }

        for intent in intents:
            if intent in intent_responses:
                return random.choice(intent_responses[intent])

        response = ""
        if sentiment == "negative":
            response = "I'm sorry you're feeling that way. How can I help?"
        elif sentiment == "positive":
            response = "Glad to hear that! How can I assist you today?"
        else:
            response = random.choice(
                RESPONSES[PERSONALITY_MODE].get(
                    "fallback", ["Can you clarify?"]
                )
            )

        logger.debug(f"Process time: {time.perf_counter() - start_time:.4f}s")
        return response

    def extract_intents(self, text: str):
        """Extracts intents using zero-shot classification with improved handling."""
        candidate_labels = [
            "greeting",
            "farewell",
            "appointment",
            "pricing",
            "services",
            "small talk",
        ]
        try:
            result = classifier(text, candidate_labels)
            return [
                label
                for label, score in zip(result["labels"], result["scores"])
                if score > 0.5
            ]
        except Exception as e:
            logger.error(f"Intent extraction failed: {e}")
            return []

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """Analyzes sentiment and returns 'positive', 'neutral', or 'negative'."""
        scores = analyzer.polarity_scores(text)
        return (
            "positive"
            if scores["compound"] >= 0.05
            else "negative" if scores["compound"] <= -0.05 else "neutral"
        )
