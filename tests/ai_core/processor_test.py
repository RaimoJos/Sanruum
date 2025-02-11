# tests\ai_core\processor_test.py
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from sanruum.ai_core.memory import AIMemory
from sanruum.ai_core.processor import AIProcessor


@pytest.fixture
def processor() -> AIProcessor:
    """Fixture for AIProcessor"""
    memory = MagicMock(spec=AIMemory)
    return AIProcessor(memory)


def test_process_input_greeting(
        processor: AIProcessor, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if AI processor correctly handles a greeting"""
    monkeypatch.setattr(processor.memory, 'store_message', MagicMock())
    response = processor.process_input('Hello')
    assert 'Hello!' in response


def test_process_input_farewell(
        processor: AIProcessor, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if AI processor correctly handles a farewell"""
    monkeypatch.setattr(processor.memory, 'store_message', MagicMock())
    response = processor.process_input('Goodbye')
    assert 'Goodbye!' in response


def test_process_input_appointment(
        processor: AIProcessor, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if AI processor correctly handles an appointment query"""
    monkeypatch.setattr(processor.memory, 'store_message', MagicMock())
    response = processor.process_input('I want to book an appointment')
    assert 'Would you like to book an appointment?' in response


def test_process_input_pricing(
        processor: AIProcessor, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if AI processor correctly handles a pricing query"""
    monkeypatch.setattr(processor.memory, 'store_message', MagicMock())
    response = processor.process_input('What is the pricing?')
    assert 'Our pricing depends' in response


def test_process_input_sentiment_positive(
        processor: AIProcessor, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if AI processor handles positive sentiment correctly"""
    monkeypatch.setattr(processor.memory, 'store_message', MagicMock())
    response = processor.process_input("I'm happy with the service!")
    assert 'Glad to hear that!' in response


def test_process_input_sentiment_negative(
        processor: AIProcessor, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if AI processor handles negative sentiment correctly"""
    monkeypatch.setattr(processor.memory, 'store_message', MagicMock())
    response = processor.process_input("I'm not happy at all.")
    assert "I'm sorry you're feeling that way." in response


def test_extract_intents(processor: AIProcessor) -> None:
    """Test intent extraction logic"""
    response = processor.extract_intents('I want to book an appointment')
    assert 'appointment' in response
