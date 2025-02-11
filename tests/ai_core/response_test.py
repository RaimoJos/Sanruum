from __future__ import annotations

from typing import cast
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture

from sanruum.ai_core.memory import AIMemory
from sanruum.ai_core.processor import AIProcessor
from sanruum.ai_core.response import AIResponse
from sanruum.faq_handler import FAQHandler
from sanruum.utils.logger import logger

# Disable logger to prevent noise in test output
logger.disabled = True


@pytest.fixture
def ai_response() -> AIResponse:
    """Fixture to provide an AIResponse instance with proper mocks."""
    ai = AIResponse()

    # Use MagicMock with spec to have proper method signatures
    ai.memory = MagicMock(spec=AIMemory)
    ai.faq = MagicMock(spec=FAQHandler)
    ai.processor = MagicMock(spec=AIProcessor)

    # Explicitly assign mocks to methods and cast them as MagicMock
    ai.memory.find_relevant_knowledge = cast(MagicMock, MagicMock(return_value=None))
    ai.memory.store_knowledge = cast(MagicMock, MagicMock())
    ai.faq.get_answer = cast(MagicMock, MagicMock(return_value=None))
    ai.processor.process_input = cast(
        MagicMock, MagicMock(return_value='Processed response'),
    )

    return ai


# Test when the response is cached
def test_cache_hit(mocker: MockerFixture, ai_response: AIResponse) -> None:
    ai_response.response_cache = {'hello': 'Hi there!'}

    # Calling get_response with a cached input
    result = ai_response.get_response('hello')

    # Check that the result is from the cache
    assert result == 'Hi there!'

    # Use cast to tell mypy these are MagicMock objects
    cast(MagicMock, ai_response.memory.find_relevant_knowledge).assert_not_called()
    cast(MagicMock, ai_response.faq.get_answer).assert_not_called()


# Test when the response is found in memory
def test_memory_hit(ai_response: AIResponse) -> None:
    cast(
        MagicMock,
        ai_response.memory.find_relevant_knowledge,
    ).return_value = 'Relevant memory response'

    result = ai_response.get_response('memory_question')

    assert result == 'Relevant memory response'
    cast(MagicMock, ai_response.memory.find_relevant_knowledge).assert_called_once_with(
        'memory_question',
    )
    cast(MagicMock, ai_response.faq.get_answer).assert_not_called()


# Test when the response is found in FAQ
def test_faq_hit(ai_response: AIResponse) -> None:
    cast(MagicMock, ai_response.faq.get_answer).return_value = 'FAQ response'
    cast(MagicMock, ai_response.memory.find_relevant_knowledge).return_value = None

    result = ai_response.get_response('faq_question')

    assert result == 'FAQ response'
    cast(MagicMock, ai_response.memory.store_knowledge).assert_called_once_with(
        'faq_question', 'FAQ response',
    )
    # Ensure response is cached
    assert ai_response.response_cache['faq_question'] == 'FAQ response'


# Test when the response is processed by the AI processor
def test_ai_processor_response(ai_response: AIResponse) -> None:
    cast(
        MagicMock,
        ai_response.processor.process_input,
    ).return_value = 'AI processed response'
    cast(MagicMock, ai_response.memory.find_relevant_knowledge).return_value = None
    cast(MagicMock, ai_response.faq.get_answer).return_value = None

    result = ai_response.get_response('processor_question')

    assert result == 'AI processed response'
    cast(MagicMock, ai_response.processor.process_input).assert_called_once_with(
        'processor_question',
    )
    cast(MagicMock, ai_response.memory.store_knowledge).assert_called_once_with(
        'processor_question', 'AI processed response',
    )
    # Ensure response is cached
    assert ai_response.response_cache['processor_question'] == 'AI processed response'


# Test when an error occurs during response generation
@patch('sanruum.ai_core.response.logger')
def test_error_handling(mock_logger: MagicMock, ai_response: AIResponse) -> None:
    # Mock an exception in response generation
    cast(
        MagicMock,
        ai_response.processor.process_input,
    ).side_effect = Exception('Test error')

    result = ai_response.get_response('error_question')

    # Check that the error was logged
    cast(MagicMock, mock_logger.error).assert_called()

    logged_message = mock_logger.error.call_args[0][0]  # Get the actual log message
    assert '❌ Error processing response: Test error' in logged_message

    # Check the fallback response
    assert result == (
        "I'm experiencing some issues at the moment."
        ' Please try again later!'
    )
