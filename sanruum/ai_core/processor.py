import random
from typing import Dict, List

import spacy
import torch
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sanruum.ai_core.config import RESPONSES, PERSONALITY_MODE
from sanruum.ai_core.memory import AIMemory
from sanruum.utils.logger import logger  # Added logging support

# Initialize Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")  # Debugging output

# Load AI Models
analyzer = SentimentIntensityAnalyzer()
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0 if device.type == "cuda" else -1
)

try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    logger.error(f"Failed to load Spacy NLP model: {e}")
    nlp = None  # Prevent crashes if model fails to load


class AIProcessor:
    def __init__(self, memory: AIMemory) -> None:
        self.memory = memory
        self.context = []

    def process_input(self, user_input: str) -> str:
        """Processes user input and determines AI response."""
        user_input = user_input.strip().lower()
        self.memory.store_message("user", user_input)

        # Check stored knowledge
        if knowledge_response := self.memory.find_relevant_knowledge(user_input):
            return f"I remember something about that: {knowledge_response}"

        sentiment = self.analyze_sentiment(user_input)
        reminders = self.memory.get_reminders()

        intents = self.extract_intents(user_input)

        def safe_choice(options: List[str]) -> str:
            return random.choice(options) if options else "I didn't understand that."

        if "greeting" in intents:
            return safe_choice(RESPONSES[PERSONALITY_MODE].get("greeting", ["Hello!"]))
        if "farewell" in intents:
            return safe_choice(RESPONSES[PERSONALITY_MODE].get("farewell", ["Goodbye!"]))
        if "appointment" in intents:
            return "Would you like to book an appointment? 📅"
        if {"pricing", "services"}.issubset(intents):
            return "Our pricing depends on the service package you choose. Would you like more details?"
        if reminders:
            return f"Just a quick reminder: {reminders[0]}"

        # Sentiment-based response
        if sentiment == "negative":
            return "I'm really sorry you're feeling that way. How can I help you?"
        elif sentiment == "positive":
            return "I'm glad to hear you're feeling good! What can I do for you today?"
        else:
            return safe_choice(RESPONSES[PERSONALITY_MODE].get("fallback", ["Can you clarify?"]))

    @staticmethod
    def extract_intents(text: str) -> List[str]:
        """Extracts intents using zero-shot classification."""
        candidate_labels = ["greeting", "farewell", "appointment", "pricing", "services", "small talk"]
        try:
            result = classifier(text, candidate_labels)
            return [label for label, score in zip(result["labels"], result["scores"]) if score > 0.4]
        except Exception as e:
            logger.error(f"Intent extraction failed: {e}")
            return []

    def generate_dynamic_response(self, user_input: str) -> str:
        """Generates a more dynamic response based on conversation history."""
        last_message = self.memory.get_last_message()

        if last_message and "?" in last_message:
            return "Interesting! Tell me more. 🤔"

        return random.choice([
            "I'm still learning! What else can I help with?",
            "That's a good question! Let me think...",
            "I'm here to help. Can you clarify a bit?"
        ])

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """Analyzes the sentiment and returns 'positive', 'neutral', or 'negative'."""
        scores: Dict[str, float] = analyzer.polarity_scores(text)
        if scores["compound"] >= 0.05:
            return "positive"
        elif scores["compound"] <= -0.05:
            return "negative"
        return "neutral"
