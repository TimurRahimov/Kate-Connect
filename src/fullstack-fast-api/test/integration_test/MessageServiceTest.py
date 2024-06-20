from uuid import uuid4

import pytest

from src.dependency_injection import ServiceContainer
from src.domain import DomainRegister
from src.domain.abstractions.repositories import IChatRepository
from src.domain.abstractions.services import IChatService, IUserService, IMessageService
from src.domain.models import ChatType
from test.integration_test.infrastructure import TestInfrastructureRegister


@pytest.fixture
def anyio_backend():
    return 'asyncio'


TestInfrastructureRegister.register()
DomainRegister.register()
chat_repo = ServiceContainer.get(IChatRepository)
user_service = ServiceContainer.get(IUserService)
chat_service = ServiceContainer.get(IChatService)
message_service = ServiceContainer.get(IMessageService)


@pytest.mark.anyio
async def test_send_message():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    session = user_model1.session

    chat_model = await chat_service.create_chat(session=session,
                                                members_id=[user_model2.user_id],
                                                chat_type=ChatType.PERSONAL_CHAT)

    # Act
    message = await message_service.send_message(session=session, chat_id=chat_model.chat_id)
    query_message = await message_service.get_message(session=session, chat_id=chat_model.chat_id,
                                                      message_id=message.message_id)

    # Assert
    assert message is not None
    assert query_message.message_id == message.message_id
    assert len(query_message.encodings) == 0
    assert len(query_message.attachments) == 0


@pytest.mark.anyio
async def test_send_message_stranger():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model3 = await user_service.register(uuid4().hex, 'PASSWORD')
    session_1 = user_model1.session
    session_3 = user_model3.session

    chat_model = await chat_service.create_chat(session=session_1,
                                                members_id=[user_model2.user_id],
                                                chat_type=ChatType.PERSONAL_CHAT)

    # Act
    message = await message_service.send_message(session=session_3, chat_id=chat_model.chat_id)

    # Assert
    assert message is None


@pytest.mark.anyio
async def test_query_message_stranger():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model3 = await user_service.register(uuid4().hex, 'PASSWORD')
    session_1 = user_model1.session
    session_3 = user_model3.session

    chat_model = await chat_service.create_chat(session=session_1,
                                                members_id=[user_model2.user_id],
                                                chat_type=ChatType.PERSONAL_CHAT)

    # Act
    message = await message_service.send_message(session=session_1, chat_id=chat_model.chat_id)
    query_message = await message_service.get_message(session=session_3, chat_id=chat_model.chat_id,
                                                      message_id=message.message_id)

    # Assert
    assert message is not None
    assert query_message is None


@pytest.mark.anyio
async def test_shown_message():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    session_1 = user_model1.session
    session_2 = user_model2.session

    chat_model = await chat_service.create_chat(session=session_1,
                                                members_id=[
                                                    user_model2.user_id
                                                ],
                                                chat_type=ChatType.PERSONAL_CHAT)

    # Act
    message = await message_service.send_message(session=session_1, chat_id=chat_model.chat_id)
    query_message_before = await message_service.get_message(session=session_1, chat_id=chat_model.chat_id,
                                                             message_id=message.message_id)
    await message_service.set_shown(session=session_2, chat_id=chat_model.chat_id, message_id=message.message_id)
    query_message_after = await message_service.get_message(session=session_1, chat_id=chat_model.chat_id,
                                                            message_id=message.message_id)

    # Assert
    assert query_message_before.shown_list == []
    assert query_message_after.shown_list == [user_model2.user_id]


@pytest.mark.anyio
async def test_shown_self_message():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    session_1 = user_model1.session

    chat_model = await chat_service.create_chat(session=session_1,
                                                members_id=[
                                                    user_model2.user_id
                                                ],
                                                chat_type=ChatType.PERSONAL_CHAT)

    # Act
    message = await message_service.send_message(session=session_1, chat_id=chat_model.chat_id)
    query_message_before = await message_service.get_message(session=session_1, chat_id=chat_model.chat_id,
                                                             message_id=message.message_id)
    await message_service.set_shown(session=session_1, chat_id=chat_model.chat_id, message_id=message.message_id)
    query_message_after = await message_service.get_message(session=session_1, chat_id=chat_model.chat_id,
                                                            message_id=message.message_id)

    # Assert
    assert query_message_before.shown_list == []
    assert query_message_after.shown_list == []
