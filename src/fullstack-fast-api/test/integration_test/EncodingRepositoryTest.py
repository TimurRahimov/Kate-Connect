from uuid import uuid4

import pytest

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.repositories import IEncodingRepository
from src.domain.entities import MessageEncodingEntity
from test.integration_test.infrastructure import TestInfrastructureRegister


@pytest.fixture
def anyio_backend():
    return 'asyncio'


TestInfrastructureRegister.register()
encoding_repo = ServiceContainer.get(IEncodingRepository)


@pytest.mark.anyio
async def test_add_query_encoding():
    # Arrange
    message_id = uuid4().hex
    for_id_N1 = uuid4().hex
    for_id_N2 = uuid4().hex

    encoding_entity_N1 = MessageEncodingEntity(
        encoding_id=uuid4().hex,
        message_id=message_id,
        for_id=for_id_N1,
        encoding=""
    )

    # Act
    await encoding_repo.add(encoding_entity_N1)
    query_encoding_N1 = await encoding_repo.query(message_id, for_id_N1)
    query_encoding_N2 = await encoding_repo.query(message_id, for_id_N2)

    # Assert
    assert query_encoding_N1 is not None
    assert query_encoding_N2 is None


@pytest.mark.anyio
async def test_delete_encoding():
    # Arrange
    message_id = uuid4().hex
    for_id = uuid4().hex

    encoding_entity = MessageEncodingEntity(
        encoding_id=uuid4().hex,
        message_id=message_id,
        for_id=for_id,
        encoding=""
    )

    # Act
    await encoding_repo.add(encoding_entity)
    query_encoding_before = await encoding_repo.query(message_id, for_id)
    await encoding_repo.delete(message_id, for_id)
    query_encoding_after = await encoding_repo.query(message_id, for_id)

    # Assert
    assert query_encoding_before is not None
    assert query_encoding_after is None
