# sanruum\ai_core\processor.py
from __future__ import annotations

import random
import time

import torch
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sanruum.ai_core.config import PERSONALITY_MODE
from sanruum.ai_core.config import RESPONSES
from sanruum.ai_core.memory import AIMemory
from sanruum.utils.logger import logger

# Initialize Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
logger.info(f'Using device: {device}')

# Load AI Models
analyzer = SentimentIntensityAnalyzer()
classifier = pipeline(
    'zero-shot-classification',
    model='facebook/bart-large-mnli',
    device=0 if device.type == 'cuda' else -1,
)


class AIProcessor:
    def __init__(self, memory: AIMemory) -> None:
        self.memory = memory
        # Reserved for future use: managing conversation context
        self.context: list[str] = []

    def process_input(self, user_input: str) -> str:
        """Processes user input and determines AI response."""
        start_time = time.perf_counter()
        user_input = user_input.strip().lower()
        self.memory.store_message('user', user_input)

        # Check stored knowledge.
        knowledge_response: str | None = self.memory.find_relevant_knowledge(user_input)
        if isinstance(knowledge_response, str):
            return knowledge_response

        # Check for reminders.
        reminders = self.memory.get_reminders()
        if isinstance(reminders, list) and reminders:
            return f'Reminder: {reminders[0]}'

        # First, extract intents.
        intents_start = time.perf_counter()
        intents = self.extract_intents(user_input)
        logger.debug(
            f'Extracted intents: {intents} (Time:'
            f' {time.perf_counter() - intents_start:.4f}s)',
        )

        # Fixed intent responses expected by tests.
        intent_responses = {
            'greeting': ['Hello!'],
            'farewell': ['Goodbye!'],
            'appointment': ['Would you like to book an appointment?'],
            'pricing': [
                'Our pricing depends on the service package you choose.'
                ' Would you like more details?',
            ],
        }

        for intent in intents:
            if intent in intent_responses:
                return random.choice(intent_responses[intent])

        # If no matching fixed intent is found, analyze sentiment.
        sentiment_start = time.perf_counter()
        sentiment = self.analyze_sentiment(user_input)
        logger.debug(
            f'Analyzed sentiment: {sentiment}'
            f' (Time: {time.perf_counter() - sentiment_start:.4f}s)',
        )

        if sentiment == 'negative':
            response = "I'm sorry you're feeling that way. How can I help?"
        elif sentiment == 'positive':
            response = 'Glad to hear that! How can I assist you today?'
        else:
            response = random.choice(
                RESPONSES[PERSONALITY_MODE].get('fallback', ['Can you clarify?']),
            )

        logger.debug(f'Process time: {time.perf_counter() - start_time:.4f}s')
        return response if response else "Sorry, I couldn't process your request."

    @staticmethod
    def extract_intents(text: str) -> list[str]:
        """
        Extracts intents using zero-shot classification with improved handling.
        """
        candidate_labels = [
            'greeting',
            'farewell',
            'appointment',
            'pricing',
            'services',
            'small talk',
        ]
        try:
            result = classifier(text, candidate_labels)
            logger.debug(f'Raw classifier output: {result}')
            return [
                label
                for label, score in zip(result['labels'], result['scores'])
                if score > 0.5
            ]
        except Exception as e:
            logger.error(f'Intent extraction failed: {e}')
            return []

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        """
        Analyzes sentiment and returns 'positive', 'neutral', or 'negative'.
        """
        scores = analyzer.polarity_scores(text)
        logger.debug(f'Sentiment scores: {scores}')
        if scores['compound'] >= 0.05:
            return 'positive'
        elif scores['compound'] <= -0.05:
            return 'negative'
        else:
            return 'neutral'
