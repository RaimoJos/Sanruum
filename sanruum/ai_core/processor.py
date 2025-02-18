# sanruum\ai_core\processor.py
from __future__ import annotations

import random
import time

import torch
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sanruum.ai_core.config import INTENTS
from sanruum.ai_core.config import PERSONALITY_MODE
from sanruum.ai_core.memory import AIMemory
from sanruum.nlp.utils.preprocessing import preprocess_text
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

        # Preprocess input and ensure it's a string
        processed_input = preprocess_text(user_input, return_string=True)

        if isinstance(processed_input, list):
            # Convert list to a single string
            processed_input = ' '.join(processed_input)

        user_input = processed_input

        # Ensure it's a string (for type safety and checking)
        assert isinstance(
            user_input, str,
        ), f'Expected user_input to be a string, got {type(user_input)}'

        # Append to context (which is always a list of strings now)
        self.context.append(user_input)
        self.context = self.context[-10:]  # Keep only the last 10 items in context
        self.memory.store_message('user', user_input)

        # Check stored knowledge.
        knowledge_response: str = str(self.memory.find_relevant_knowledge(user_input))

        # Ensure knowledge_response is a string (join list if it's a list of strings).
        if isinstance(knowledge_response, list):
            knowledge_response = ' '.join(knowledge_response)

        # Now knowledge_response is guaranteed to be a str.
        if not knowledge_response:
            knowledge_response = "Sorry, I didn't find anything relevant."

        # Check for reminders.
        reminders = self.memory.get_reminders() or []
        if reminders:
            return f'Reminder: {reminders[0]}'

        # Extract intents.
        intents_start = time.perf_counter()
        intents = self.extract_intents(user_input)
        logger.debug(
            f'Extracted intents: {intents} '
            f'(Time: {time.perf_counter() - intents_start:.4f}s)',
        )

        # Intent-based responses.
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

        # If no intent matched, analyze sentiment.
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
            # Fallback response if sentiment is neutral.
            fallback_responses = INTENTS[PERSONALITY_MODE].get(
                'fallback', ['Can you clarify?'],
            )
            response = str(
                random.choice(fallback_responses) if fallback_responses
                else "Sorry, I didn't understand that.",
            )

        logger.debug(f'Process time: {time.perf_counter() - start_time:.4f}s')
        return response

    @staticmethod
    def extract_intents(text: str) -> str:
        """Extract intents from the input text."""
        try:
            result = classifier(
                text,
                candidate_labels=list(INTENTS.keys()),  # List of possible intents
            )
            intents = result['labels']

            # Ensure we always return a string
            if isinstance(intents, list):
                return intents[0] if intents else ''
            return str(intents)  # If it's a single string, just return it
        except Exception as e:
            logger.error(f'Error extracting intents: {str(e)}')
            return ''  # Ensure a string is returned even on error

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
