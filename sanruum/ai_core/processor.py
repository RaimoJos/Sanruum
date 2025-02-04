import random
from typing import Dict, List, Optional

import spacy
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sanruum.ai_core.config import PERSONALITY_MODE, RESPONSES
from sanruum.ai_core.memory import AIMemory

analyzer = SentimentIntensityAnalyzer()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
nlp = spacy.load("en_core_web_sm")


class AIProcessor:
    def __init__(self, memory: AIMemory) -> None:
        self.memory: AIMemory = memory

    def process_input(self, user_input: str) -> str:
        """Processes user input and determines AI response based on intent."""
        self.memory.store_message("user", user_input)

        sentiment: str = str(self.analyze_sentiment(user_input))  # Ensure it returns str
        reminders: List[str] = self.memory.get_reminders()
        user_input = user_input.lower()

        doc = nlp(user_input)
        intents: List[str] = self.extract_intents(doc.text) or []  # Ensure it’s a list

        # Ensure RESPONSES return a string
        def safe_choice(options: List[str]) -> str:
            return str(random.choice(options)) if options else "I didn't understand that."

        if "greeting" in intents:
            return safe_choice(RESPONSES[PERSONALITY_MODE].get("greeting", ["Hello!"]))

        if "farewell" in intents:
            return safe_choice(RESPONSES[PERSONALITY_MODE].get("farewell", ["Goodbye!"]))

        if "appointment" in intents:
            return "Would you like to book an appointment? 📅"

        if "pricing" in intents and "services" in intents:
            return "Our pricing depends on the service package you choose. Would you like more details?"

        if reminders:
            return f"Just a quick reminder: {reminders[0]}"

        if sentiment == "negative":
            return "I'm really sorry you're feeling that way. How can I help you?"
        elif sentiment == "positive":
            return "I'm glad to hear you're feeling good! What can I do for you today?"
        else:
            return safe_choice(RESPONSES[PERSONALITY_MODE].get("fallback", ["Can you clarify?"]))

    def generate_dynamic_response(self, user_input: str) -> str:
        """Generates a more dynamic response based on conversation history."""
        last_message: Optional[str] = self.memory.get_last_message()  # Ensure it's a string

        if last_message and "?" in last_message:  # Check string directly
            return "Interesting! Tell me more. 🤔"

        return random.choice([
            "I'm still learning! What else can I help with?",
            "That's a good question! Let me think...",
            "I'm here to help. Can you clarify a bit?"
        ])

    @staticmethod
    def extract_intents(text: str) -> List[str]:
        """Extracts intents using zero-shot classification."""
        candidate_labels = ["greeting", "farewell", "appointment", "pricing", "small talk"]
        result = classifier(text, candidate_labels)
        labels: List[str] = result.get("labels", [])
        scores: List[float] = result.get("scores", [])

        return [label for label, score in zip(labels, scores) if score > 0.5]

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """Analyzes the sentiment and returns 'positive', 'neutral', or 'negative'."""
        scores: Dict[str, float] = analyzer.polarity_scores(text)
        if scores["compound"] >= 0.05:
            return "positive"
        elif scores["compound"] <= -0.05:
            return "negative"
        return "neutral"
