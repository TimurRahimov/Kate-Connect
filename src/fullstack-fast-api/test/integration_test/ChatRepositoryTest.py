from uuid import uuid4

import pytest

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.repositories import IChatRepository
from src.domain.entities import ChatEntity
from src.domain.models import ChatType
from test.integration_test.infrastructure import TestInfrastructureRegister


@pytest.fixture
def anyio_backend():
    return 'asyncio'


TestInfrastructureRegister.register()
chat_repo = ServiceContainer.get(IChatRepository)


@pytest.mark.anyio
async def test_add_chat():
    # Arrange
    chat_id = uuid4().hex
    user_id = uuid4().hex
    chat_entity = ChatEntity(
        chat_id=chat_id,
        chat_type=ChatType.PERSONAL_CHAT,
        members=[user_id]
        # title: str | None = None
        # avatar_url: str = ""
    )

    # Act
    await chat_repo.add(chat_entity)

    # Assert
    assert await chat_repo.query(chat_id) is not None
    assert (await chat_repo.query(chat_id)).chat_type == ChatType.PERSONAL_CHAT
    assert user_id in (await chat_repo.query(chat_id)).members


@pytest.mark.anyio
async def test_edit_chat():
    # Arrange
    chat_id = uuid4().hex
    user_id = uuid4().hex
    chat_entity = ChatEntity(
        chat_id=chat_id,
        chat_type=ChatType.PERSONAL_CHAT,
        members=[user_id]
    )

    # Act
    await chat_repo.add(chat_entity)
    query_chat = await chat_repo.query(chat_id)
    query_chat.title = "TEST_TITLE"
    query_chat.avatar_url = "TEST_AVATAR"
    await chat_repo.add(query_chat)

    # Assert
    assert (await chat_repo.query(chat_id)).title == "TEST_TITLE"
    assert (await chat_repo.query(chat_id)).avatar_url == "TEST_AVATAR"


@pytest.mark.anyio
async def test_get_user_chats():
    # Arrange
    user_id = uuid4().hex

    chat_id_N1 = uuid4().hex
    chat_entity_N1 = ChatEntity(
        chat_id=chat_id_N1,
        chat_type=ChatType.PERSONAL_CHAT,
        members=[user_id, uuid4().hex]
    )

    chat_id_N2 = uuid4().hex
    chat_entity_N2 = ChatEntity(
        chat_id=chat_id_N2,
        chat_type=ChatType.PERSONAL_CHAT,
        members=[user_id, uuid4().hex]
    )

    # Act
    await chat_repo.add(chat_entity_N1)
    await chat_repo.add(chat_entity_N2)
    user_chats = list((await chat_repo.get_user_chats(user_id)).keys())

    # Assert
    assert chat_id_N1 in user_chats
    assert chat_id_N2 in user_chats


@pytest.mark.anyio
async def test_delete_chat():
    # Arrange
    chat_id = uuid4().hex
    user_id = uuid4().hex
    chat_entity = ChatEntity(
        chat_id=chat_id,
        chat_type=ChatType.PERSONAL_CHAT,
        members=[user_id]
    )

    # Act
    await chat_repo.add(chat_entity)
    query_chat_before = await chat_repo.query(chat_id)
    await chat_repo.delete(chat_id)
    query_chat_after = await chat_repo.query(chat_id)

    # Assert
    assert query_chat_before is not None
    assert query_chat_after is None
