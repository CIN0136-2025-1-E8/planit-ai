import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.crud.chat_crud import chat_crud
from tests.mock_models import TestBase, MockUser, MockChatMessage, MockChatMessageSchema, MockChatRole


@pytest.fixture(scope="function")
def test_db_session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestBase.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        TestBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def mock_chat_model(monkeypatch):
    monkeypatch.setattr(chat_crud, 'model', MockChatMessage)


@pytest.fixture(scope="function")
def test_user(test_db_session: Session) -> MockUser:
    user = MockUser(
        uuid=str(uuid.uuid4()),
        name="Test User",
        email="test@example.com",
        hashed_password="fake_password"
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


def test_get_chat_history(test_db_session: Session, test_user: MockUser, mock_chat_model):
    msg1 = MockChatMessage(uuid=str(uuid.uuid4()), role="user", text="Hello", order=0, owner_uuid=test_user.uuid)
    msg2 = MockChatMessage(uuid=str(uuid.uuid4()), role="model", text="Hi there!", order=1, owner_uuid=test_user.uuid)
    test_db_session.add_all([msg1, msg2])
    test_db_session.commit()

    history = chat_crud.get_chat_history(db=test_db_session, user_uuid=test_user.uuid)

    assert len(history) == 2
    assert history[0].text == "Hello"
    assert history[1].role == "model"
    assert history[1].order == 1


def test_get_empty_chat_history(test_db_session: Session, test_user: MockUser, mock_chat_model):
    history = chat_crud.get_chat_history(db=test_db_session, user_uuid=test_user.uuid)

    assert history == []


def test_append_chat_history(test_db_session: Session, test_user: MockUser, mock_chat_model):
    new_message = MockChatMessageSchema(role=MockChatRole.USER, text="First message")

    chat_crud.append_chat_history(db=test_db_session, user_uuid=test_user.uuid, obj_in=new_message)

    db_user = test_db_session.get(MockUser, test_user.uuid)
    assert len(db_user.chat_history) == 1
    assert db_user.chat_history[0].text == "First message"
    assert db_user.chat_history[0].order == 0

    second_message = MockChatMessageSchema(role=MockChatRole.MODEL, text="Second message")
    chat_crud.append_chat_history(db=test_db_session, user_uuid=test_user.uuid, obj_in=second_message)

    test_db_session.refresh(db_user)
    assert len(db_user.chat_history) == 2
    assert db_user.chat_history[1].text == "Second message"
    assert db_user.chat_history[1].order == 1


def test_delete_chat_history(test_db_session: Session, test_user: MockUser, mock_chat_model):
    msg1 = MockChatMessage(uuid=str(uuid.uuid4()), role="user", text="To be deleted 1", order=0, owner_uuid=test_user.uuid)
    msg2 = MockChatMessage(uuid=str(uuid.uuid4()), role="model", text="To be deleted 2", order=1, owner_uuid=test_user.uuid)
    test_db_session.add_all([msg1, msg2])
    test_db_session.commit()
    assert len(test_user.chat_history) == 2

    num_deleted = chat_crud.delete_chat_history(db=test_db_session, user_uuid=test_user.uuid)

    test_db_session.refresh(test_user)
    assert num_deleted == 2
    assert len(test_user.chat_history) == 0
    assert test_db_session.query(MockChatMessage).count() == 0


def test_delete_chat_history_isolates_users(test_db_session: Session, test_user: MockUser, mock_chat_model):
    user2 = MockUser(
        uuid=str(uuid.uuid4()),
        name="Other User",
        email="other@example.com",
        hashed_password="another_password"
    )
    test_db_session.add(user2)
    msg1 = MockChatMessage(uuid=str(uuid.uuid4()), role="user", text="user1 message", order=0, owner_uuid=test_user.uuid)
    msg2 = MockChatMessage(uuid=str(uuid.uuid4()), role="model", text="user2 message", order=0, owner_uuid=user2.uuid)
    test_db_session.add_all([msg1, msg2])
    test_db_session.commit()
    assert test_db_session.query(MockChatMessage).count() == 2

    num_deleted = chat_crud.delete_chat_history(db=test_db_session, user_uuid=test_user.uuid)

    assert num_deleted == 1
    assert test_db_session.query(MockChatMessage).count() == 1
    remaining_message = test_db_session.query(MockChatMessage).one()
    assert remaining_message.owner_uuid == user2.uuid