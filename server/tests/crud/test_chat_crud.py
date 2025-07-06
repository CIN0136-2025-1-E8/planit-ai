import os
import pickle

import pytest
from google.genai.types import Content, Part

from app.crud.chat_crud import CRUDChat
from schemas import ChatMessage, ChatRole


@pytest.fixture
def mock_paths(tmp_path):
    context_path = tmp_path / "test_context.pkl"
    history_path = tmp_path / "test_history.pkl"
    return str(context_path), str(history_path)


@pytest.fixture
def crud_chat(mock_paths):
    context_path, history_path = mock_paths
    return CRUDChat(llm_context_file_path=context_path, chat_history_file_path=history_path)


def test_initialization_with_no_files(crud_chat):
    assert crud_chat.llm_context == []
    assert crud_chat.chat_history == []


def test_read_llm_context_from_existing_file(mock_paths):
    context_path, history_path = mock_paths
    mock_context_data = [Content(role="user", parts=[Part(text="Mock message.")])]
    with open(context_path, "wb") as f:
        # noinspection PyTypeChecker
        pickle.dump(mock_context_data, f)

    crud = CRUDChat(llm_context_file_path=context_path, chat_history_file_path=history_path)

    assert crud.get_llm_context() == mock_context_data


def test_write_llm_context(crud_chat, mock_paths):
    context_path, _ = mock_paths
    mock_context_data = [Content(role="user", parts=[Part(text="Mock message.")])]
    crud_chat.llm_context = mock_context_data

    crud_chat.write_llm_context_to_file(file_path=context_path)

    assert os.path.exists(context_path)
    with open(context_path, "rb") as f:
        assert pickle.load(f) == mock_context_data


def test_get_llm_context(crud_chat):
    new_content = [Content(role="user", parts=[Part(text="Mock content.")])]
    crud_chat.llm_context = new_content

    assert crud_chat.get_llm_context() == new_content


def test_append_llm_context(crud_chat):
    new_content = [Content(role="user", parts=[Part(text="Mock message.")])]

    crud_chat.append_llm_context(new_content)
    assert crud_chat.get_llm_context() == [new_content[0]]

    crud_chat.append_llm_context(new_content)
    assert crud_chat.get_llm_context() == [new_content[0], new_content[0]]


def test_read_chat_history_from_existing_file(mock_paths):
    context_path, history_path = mock_paths
    mock_history_data = [ChatMessage(role=ChatRole.MODEL, text="Mock response.")]
    with open(history_path, "wb") as f:
        # noinspection PyTypeChecker
        pickle.dump(mock_history_data, f)

    crud = CRUDChat(llm_context_file_path=context_path, chat_history_file_path=history_path)

    assert crud.get_chat_history() == mock_history_data


def test_write_chat_history(crud_chat, mock_paths):
    _, history_path = mock_paths
    mock_history_data = ChatMessage(role=ChatRole.MODEL, text="Mock response.")
    crud_chat.chat_history = [mock_history_data]

    crud_chat.write_chat_history_to_file(file_path=history_path)

    assert os.path.exists(history_path)
    with open(history_path, "rb") as f:
        assert pickle.load(f) == [mock_history_data]


def test_get_chat_history(crud_chat):
    new_message = ChatMessage(role=ChatRole.USER, text="Mock message.")
    crud_chat.chat_history = [new_message]

    assert crud_chat.get_chat_history() == [new_message]


def test_append_chat_history(crud_chat):
    new_message = ChatMessage(role=ChatRole.USER, text="Mock message.")

    crud_chat.append_chat_history(new_message)
    assert crud_chat.get_chat_history() == [new_message]

    crud_chat.append_chat_history(new_message)
    assert crud_chat.get_chat_history() == [new_message, new_message]
