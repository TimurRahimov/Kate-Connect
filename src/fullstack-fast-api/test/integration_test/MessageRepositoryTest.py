from uuid import uuid4

import pytest

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.repositories import IMessageRepository
from src.domain.entities import MessageEntity
from test.integration_test.infrastructure import TestInfrastructureRegister


@pytest.fixture
def anyio_backend():
    return 'asyncio'


TestInfrastructureRegister.register()
message_repo = ServiceContainer.get(IMessageRepository)


@pytest.mark.anyio
async def test_add_message():
    # Arrange
    chat_id = uuid4().hex

    message_id_N1 = uuid4().hex
    from_id_N1 = uuid4().hex
    message_entity_N1 = MessageEntity(
        message_id=message_id_N1,
        from_id=from_id_N1,
        chat_id=chat_id,
        timestamp=""
    )
    message_id_N2 = uuid4().hex
    from_id_N2 = uuid4().hex
    message_entity_N2 = MessageEntity(
        message_id=message_id_N2,
        from_id=from_id_N2,
        chat_id=chat_id,
        timestamp=""
    )

    # Act
    await message_repo.add(message_entity_N1)
    await message_repo.add(message_entity_N2)

    # Assert
    assert await message_repo.query(chat_id, message_id_N1) is not None
    assert await message_repo.query(chat_id, message_id_N2) is not None
    assert len(await message_repo.query_last(chat_id, 10)) == 2


@pytest.mark.anyio
async def test_delete_message():
    # Arrange
    chat_id = uuid4().hex

    message_id = uuid4().hex
    from_id = uuid4().hex
    message_entity = MessageEntity(
        message_id=message_id,
        from_id=from_id,
        chat_id=chat_id,
        timestamp=""
    )

    # Act
    await message_repo.add(message_entity)
    await message_repo.delete(message_entity.chat_id, message_entity.message_id)

    # Assert
    assert await message_repo.query(chat_id, message_id) is None
    assert len(await message_repo.query_last(chat_id, 10)) == 0


@pytest.mark.anyio
async def test_update_message():
    # Arrange
    chat_id = uuid4().hex

    message_id_N1 = uuid4().hex
    from_id_N1 = uuid4().hex
    message_entity_N1 = MessageEntity(
        message_id=message_id_N1,
        from_id=from_id_N1,
        chat_id=chat_id,
        timestamp=""
    )

    message_id_N2 = uuid4().hex
    from_id_N2 = uuid4().hex
    message_entity_N2 = MessageEntity(
        message_id=message_id_N2,
        from_id=from_id_N2,
        chat_id=chat_id,
        timestamp=""
    )

    # Act
    await message_repo.add(message_entity_N1)
    await message_repo.add(message_entity_N2)
    query_message_N1 = await message_repo.query(chat_id, message_id_N1)
    query_message_N2 = await message_repo.query(chat_id, message_id_N2)
    query_message_N1.shown_list.append(from_id_N2)
    query_message_N2.edited = True
    await message_repo.update(query_message_N1)
    await message_repo.update(query_message_N2)

    # Assert
    assert (await message_repo.query(chat_id, message_id_N1)).shown_list == [from_id_N2]
    assert (await message_repo.query(chat_id, message_id_N2)).edited is True


@pytest.mark.anyio
async def test_query_last():
    # Arrange
    chat_id = uuid4().hex

    # Act
    for i in range(100):
        await message_repo.add(MessageEntity(
            message_id=i,
            from_id=uuid4().hex,
            chat_id=chat_id,
            timestamp=""
        ))

    # Assert
    assert len(await message_repo.query_last(chat_id, 1)) == 1
    assert len(await message_repo.query_last(chat_id, 4)) == 4
    assert len(await message_repo.query_last(chat_id, 10)) == 10
    assert len(await message_repo.query_last(chat_id, 50)) == 50


@pytest.mark.anyio
async def test_add_message_then_create_new_part():
    # Arrange
    chat_id = uuid4().hex

    # Act
    for i in range(311):
        await message_repo.add(MessageEntity(
            message_id=i,
            from_id=uuid4().hex,
            chat_id=chat_id,
            timestamp=""
        ))

    # Assert
    assert len(await message_repo.query_last(chat_id, 310)) == 10
