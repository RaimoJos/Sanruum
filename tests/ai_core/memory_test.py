# tests\ai_core\memory_test.py
from __future__ import annotations

import json
from unittest import mock
from unittest.mock import MagicMock

import pytest

from sanruum.ai_core.memory import AIMemory


@pytest.fixture
def memory() -> AIMemory:
    return AIMemory()  # Ensures a fresh instance for each test


# Test storing a message
@mock.patch('sanruum.ai_core.memory.AIMemory.save_memory')
def test_store_message(mock_save_memory: MagicMock) -> None:
    memory = AIMemory()
    memory.memory['history'] = []  # Ensure fresh memory state

    message = 'Hello, AI!'
    role = 'user'

    memory.store_message(role, message)

    assert len(memory.memory['history']) == 1
    assert memory.memory['history'][0]['message'] == message
    mock_save_memory.assert_called_once()


# Test loading memory with a valid filea
@mock.patch('builtins.open', new_callable=mock.mock_open, read_data='{"history": []}')
# Ensure json.load() returns a dict
@mock.patch('json.load', return_value={'history': []})
def test_load_memory_valid(
        mock_json_load: MagicMock,
        mock_open_file: MagicMock,
) -> None:
    memory = AIMemory()
    assert memory.memory == {'history': []}


# Test loading memory with a corrupted file
@mock.patch('builtins.open', new_callable=mock.mock_open, read_data='{"invalid json"}')
@mock.patch(
    'json.load',
    side_effect=json.JSONDecodeError('Expecting property name', '', 0),
)
@mock.patch('sanruum.utils.base.logger.logger.error')
def test_load_memory_corrupted(
        mock_logger_error: MagicMock,
        mock_json_load: MagicMock,
        mock_open_file: MagicMock,
) -> None:
    memory = AIMemory()
    mock_logger_error.assert_any_call(mock.ANY)  # Ensure an error was logged
    assert memory.memory == {'history': []}


# Test finding relevant knowledge
@mock.patch(
    'sanruum.ai_core.memory.AIMemory.get_all_knowledge',
    return_value={'topic1': ['info1', 'info2']},
)
def test_find_relevant_knowledge(mock_get_all_knowledge: MagicMock) -> None:
    memory = AIMemory()
    query = 'info1'

    # Debug: Manually check if data retrieval works
    knowledge_data = memory.get_all_knowledge()
    print('Knowledge from AIMemory:', knowledge_data)

    # Check if the function retrieves relevant data
    result = memory.find_relevant_knowledge(query)

    print('Query:', query)
    print('Function output:', result)

    assert result is not None, 'find_relevant_knowledge returned None'
    assert result in knowledge_data[
        'topic1'
    ], f'Expected info from topic1, but got {result}'


# Test getting the last message
def test_get_last_message() -> None:
    memory = AIMemory()
    memory.store_message('user', 'Hello, AI!')
    assert memory.get_last_message() == 'Hello, AI!'


# Test storing and retrieving knowledge
def test_store_and_retrieve_knowledge() -> None:
    memory = AIMemory()
    memory.store_knowledge('topic1', 'data1')
    assert memory.retrieve_knowledge('topic1') == ['data1']


# Test retrieving non-existent knowledge
def test_retrieve_non_existent_knowledge() -> None:
    memory = AIMemory()
    assert memory.retrieve_knowledge('unknown') is None


# Test resetting memory
@mock.patch('sanruum.ai_core.memory.AIMemory.save_memory')
def test_reset_memory(mock_save_memory: MagicMock) -> None:
    memory = AIMemory()
    memory.store_message('user', 'Hello, AI!')
    memory.store_knowledge('topic1', 'data1')
    memory.reset_memory()

    assert memory.memory == {'history': []}
    assert memory.get_reminders() == []
    mock_save_memory.assert_called()


# Test storing and retrieving reminders
def test_store_and_get_reminders() -> None:
    memory = AIMemory()
    memory.add_reminder('Buy milk')
    memory.add_reminder('Call mom')
    assert memory.get_reminders() == ['Buy milk', 'Call mom']


# Test setting and getting last intent
def test_set_and_get_last_intent() -> None:
    memory = AIMemory()
    memory.set_last_intent('greeting')
    assert memory.get_last_intent() == 'greeting'
