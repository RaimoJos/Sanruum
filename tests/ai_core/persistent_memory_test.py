from __future__ import annotations

import os
import pickle

import pytest

from sanruum.ai_core.persistent_memory import PersistentAIMemory


@pytest.fixture
def memory() -> PersistentAIMemory:  # Annotated return type for the fixture
    """Fixture for PersistentAIMemory"""
    user_id = 'test_user'
    return PersistentAIMemory(user_id)


# Added the type annotation for the argument
def test_load_user_memory(memory: PersistentAIMemory) -> None:
    """Test if user memory loads correctly"""
    assert isinstance(memory.memory, dict)
    assert 'history' in memory.memory


# Added the type annotation for the argument
def test_store_message(memory: PersistentAIMemory) -> None:
    """Test if messages are correctly stored"""
    initial_history_length = len(memory.memory['history'])
    memory.store_message('user', 'Hello!')
    assert len(memory.memory['history']) == initial_history_length + 1
    assert memory.memory['history'][-1]['message'] == 'Hello!'


# Added the type annotation for the argument
def test_persist_memory(memory: PersistentAIMemory) -> None:
    """Test if memory is correctly persisted to disk"""
    memory.store_message('user', 'This is a test.')
    memory.persist_memory()
    with open(memory.memory_file, 'rb') as file:
        memory_data, last_intent = pickle.load(file)
        assert 'history' in memory_data
        assert memory_data['history'][-1]['message'] == 'This is a test.'


# Added the type annotation for the argument
def test_reset_memory(memory: PersistentAIMemory) -> None:
    """Test if memory can be reset"""
    memory.store_message('user', 'This will be reset.')
    memory.reset_memory()
    assert memory.memory['history'] == []
    assert not os.path.exists(memory.memory_file)
