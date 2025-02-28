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
from sanruum.utils.base.logger import logger

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

        original_input = user_input
        # Preprocess input and ensure it's a string
        processed_input = preprocess_text(user_input, return_string=True)
        if isinstance(processed_input, list):
            processed_input = ' '.join(processed_input)
        user_input = processed_input

        assert isinstance(
            user_input, str,
        ), f'Expected user_input to be a string, got {type(user_input)}'

        self.context.append(user_input)
        self.context = self.context[-10:]
        self.memory.store_message('user', user_input)

        # Check stored knowledge.
        knowledge_response: str = str(self.memory.find_relevant_knowledge(user_input))
        if isinstance(knowledge_response, list):
            knowledge_response = ' '.join(knowledge_response)
        if not knowledge_response:
            knowledge_response = "Sorry, I didn't find anything relevant."

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
                candidate = random.choice(intent_responses[intent])
                # If candidate is a dict, select the personality-specific string.
                if isinstance(candidate, dict):
                    candidate = candidate.get(
                        PERSONALITY_MODE, next(iter(candidate.values())),
                    )
                return candidate

        # If no intent matched, analyze sentiment.
        sentiment_start = time.perf_counter()
        sentiment = self.analyze_sentiment(original_input)
        logger.debug(
            f'Analyzed sentiment: {sentiment}'
            f' (Time: {time.perf_counter() - sentiment_start:.4f}s)',
        )
        sentiment_scores = analyzer.polarity_scores(user_input)
        logger.debug(f'Sentiment scores: {sentiment_scores}')

        if sentiment == 'negative':
            response = "I'm sorry you're feeling that way. How can I help?"
        elif sentiment == 'positive':
            response = 'Glad to hear that! How can I assist you today?'
        else:
            fallback_responses = INTENTS.get(PERSONALITY_MODE, {}).get(
                'fallback', ['Can you clarify?'],
            )
            response = random.choice(fallback_responses)
            if isinstance(response, dict):
                response = response.get(
                    PERSONALITY_MODE, next(iter(response.values())),
                )

        logger.debug(f'Process time: {time.perf_counter() - start_time:.4f}s')
        if isinstance(response, dict):
            response = response.get(PERSONALITY_MODE, next(iter(response.values())))
        return response

    @staticmethod
    def extract_intents(text: str) -> list[str]:
        try:
            result = classifier(
                text,
                candidate_labels=list(INTENTS.keys()),
            )
            intents = result['labels']
            if isinstance(intents, list):
                return intents
            return [str(intents)]
        except Exception as e:
            logger.error(f'Error extracting intents: {str(e)}')
            return []

    @staticmethod
    def analyze_sentiment(text: str) -> str:
        scores = analyzer.polarity_scores(text)
        logger.debug(f'Sentiment scores: {scores}')
        if scores['compound'] > 0.0:
            return 'positive'
        elif scores['compound'] < 0.0:
            return 'negative'
        else:
            return 'neutral'
