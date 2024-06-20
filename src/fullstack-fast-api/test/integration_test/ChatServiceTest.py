from uuid import uuid4

import pytest

from src.dependency_injection import ServiceContainer
from src.domain import DomainRegister
from src.domain.abstractions.repositories import IChatRepository
from src.domain.abstractions.services import IChatService, IUserService
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


@pytest.mark.anyio
async def test_add_chat():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    session = user_model1.session

    # Act
    chat_model = await chat_service.create_chat(session=session,
                                                members_id=[user_model2.user_id],
                                                chat_type=ChatType.PERSONAL_CHAT)
    get_chat_model = await chat_service.get_chat(session=session, chat_id=chat_model.chat_id)

    # Assert
    assert chat_model.chat_id is not None
    assert get_chat_model is not None
    assert user_model1.user_id in [u.user_id for u in get_chat_model.members]
    assert user_model2.user_id in [u.user_id for u in get_chat_model.members]


@pytest.mark.anyio
async def test_add_personal_chat_again():
    # Arrange
    user_model1 = await user_service.register(uuid4().hex, 'PASSWORD')
    user_model2 = await user_service.register(uuid4().hex, 'PASSWORD')
    session = user_model1.session

    # Act
    chat_model_N1 = await chat_service.create_chat(session=session,
                                                   members_id=[user_model2.user_id],
                                                   chat_type=ChatType.PERSONAL_CHAT)
    chat_model_N2 = await chat_service.create_chat(session=session,
                                                   members_id=[user_model2.user_id],
                                                   chat_type=ChatType.PERSONAL_CHAT)
    get_chat_model = await chat_service.get_chat(session=session, chat_id=chat_model_N1.chat_id)

    # Assert
    assert chat_model_N1.chat_id == chat_model_N2.chat_id
    assert get_chat_model is not None
