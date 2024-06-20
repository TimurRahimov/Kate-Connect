# import pytest
#
# from src.domain.exceptions import AuthenticationError, UserNotFoundError, UserWithThisNameExistsError, \
#     PublicKeyNotFoundError
# from src.domain.requests.v1 import UserV1Model, SessionV1Model
# from test.unittests.fakers import UserV1ModelFaker, PublicKeyModelFaker
# from test.unittests.stubs import UserServiceStub
#
#
# @pytest.fixture
# def anyio_backend():
#     return 'asyncio'
#
#
# @pytest.mark.anyio
# async def test_login_success():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().model
#     user_service.user_repo.get_all.return_value = {user.user_id: user}
#
#     # Act
#     logged_user = await user_service.login(user.nickname, user.hash_of_password)
#
#     # Assert
#     user_service.user_repo.get_all.assert_called_once()
#     user_service.user_repo.add.assert_called_once()
#     user_service.publickey_repo.add.assert_not_called()
#     user_service.publickey_repo.query.assert_not_called()
#     assert len(logged_user.sessions) == 1
#     assert logged_user.user_id is not None
#     assert logged_user.last_time_online is not None
#     assert logged_user.sessions[0].last_activity is not None
#
#
# @pytest.mark.anyio
# async def test_login_raise_authentication_error():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().model
#     user_service.user_repo.get_all.return_value = {user.user_id: user}
#
#     # Act, Assert
#     with pytest.raises(AuthenticationError):
#         await user_service.login(user.nickname, '')
#
#
# @pytest.mark.anyio
# async def test_login_raise_user_not_found_error():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().model
#     user_service.user_repo.get_all.return_value = {}
#
#     # Act, Assert
#     with pytest.raises(UserNotFoundError):
#         await user_service.login(user.nickname, user.hash_of_password)
#
#
# @pytest.mark.anyio
# async def test_register_success():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().model
#     user_service.user_repo.get_all.return_value = {}
#
#     # Act
#     registered_user = await user_service.register(user.nickname, user.hash_of_password)
#
#     # Assert
#     user_service.user_repo.get_all.assert_called_once()
#     user_service.user_repo.add.assert_called_once()
#     user_service.publickey_repo.add.assert_not_called()
#     user_service.publickey_repo.query.assert_not_called()
#     assert len(registered_user.sessions) == 1
#     assert registered_user.user_id is not None
#     assert registered_user.last_time_online is not None
#     assert registered_user.sessions[0].last_activity is not None
#
#
# @pytest.mark.anyio
# async def test_register_raise_user_with_this_name_exists_error():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().model
#     user_service.user_repo.get_all.return_value = {user.user_id: user}
#
#     # Act, Assert
#     with pytest.raises(UserWithThisNameExistsError):
#         await user_service.register(user.nickname, user.hash_of_password)
#
#
# @pytest.mark.anyio
# async def test_logout_success():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().with_random_session().model
#     user_service.user_repo.get.return_value = user
#
#     # Act
#     await user_service.logout(user.sessions[0])
#
#     # Assert
#     user_service.user_repo.get.assert_called_once_with(user.user_id)
#     user_service.user_repo.add.assert_called_once_with(
#         user.copy(update={'sessions': None})
#     )
#
#
# @pytest.mark.anyio
# async def test_edit_user_success():
#     # Arrange
#     user_service = UserServiceStub()
#
#     user = UserV1ModelFaker().with_random_session().model
#     session = user.sessions[0]
#
#     new_user = UserV1ModelFaker().with_random_avatar_link().model
#     new_nickname = new_user.nickname
#     new_hash_of_password = new_user.hash_of_password
#     new_avatar_link = new_user.avatar_link
#
#     user_service.user_repo.get.return_value = user
#     user_service.session_service.verify.return_value = True
#
#     # Act
#     edited = await user_service.edit_user(
#         session,
#         nickname=new_nickname,
#         hash_of_password=new_hash_of_password,
#         avatar_link=new_avatar_link
#     )
#     edited_user: UserV1Model = user_service.user_repo.add.call_args.args[0]
#
#     # Assert
#     user_service.session_service.verify.assert_called_once()
#     user_service.user_repo.get.assert_called_once()
#     user_service.user_repo.add.assert_called_once()
#     assert edited
#     assert edited_user.nickname == new_nickname
#     assert edited_user.hash_of_password == new_hash_of_password
#     assert edited_user.avatar_link == new_avatar_link
#
#
# @pytest.mark.anyio
# async def test_edit_user_not_success():
#     # Arrange
#     user_service = UserServiceStub()
#
#     user = UserV1ModelFaker().with_random_session().model
#     another_user = UserV1ModelFaker().with_random_session().model
#     session = SessionV1Model(
#         user_id=user.user_id,
#         session_id=another_user.sessions[0].session_id,
#     )
#
#     user_service.user_repo.get.return_value = user
#     user_service.session_service.verify.return_value = False
#
#     # Act
#     edited = await user_service.edit_user(
#         session,
#         hash_of_password=another_user.hash_of_password
#     )
#
#     # Assert
#     assert not edited
#
#
# @pytest.mark.anyio
# async def test_get_public_key_success():
#     # Arrange
#     user_service = UserServiceStub()
#
#     user = UserV1ModelFaker().with_random_session().model
#     public_key = PublicKeyModelFaker(user.user_id).model
#
#     user_service.user_repo.get_safely.return_value = user
#     user_service.publickey_repo.query.return_value = public_key
#
#     # Act
#     received_public_key = await user_service.get_publickey(user.user_id)
#
#     # Assert
#     user_service.publickey_repo.query.assert_called_once()
#     assert received_public_key == public_key.public_key
#
#
# @pytest.mark.anyio
# async def test_get_public_key_raise_user_not_found_error():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().with_random_session().model
#     user_service.user_repo.get_safely.return_value = None
#
#     # Act, Assert
#     with pytest.raises(UserNotFoundError):
#         await user_service.get_publickey(user.user_id)
#
#
# @pytest.mark.anyio
# async def test_get_public_key_raise_public_key_not_found_error():
#     # Arrange
#     user_service = UserServiceStub()
#     user = UserV1ModelFaker().with_random_session().model
#     user_service.publickey_repo.query.return_value = None
#
#     # Act, Assert
#     with pytest.raises(PublicKeyNotFoundError):
#         await user_service.get_publickey(user.user_id)
#
#
# @pytest.mark.anyio
# async def test_set_public_key_success():
#     # Arrange
#     user_service = UserServiceStub()
#
#     user = UserV1ModelFaker().with_random_session().model
#     public_key = PublicKeyModelFaker(user.user_id).model
#
#     user_service.user_repo.get_safely.return_value = user
#
#     # Act
#     await user_service.set_publickey(user.user_id, user.hash_of_password, public_key.public_key)
#
#     # Assert
#     user_service.publickey_repo.add.assert_called_once_with(public_key)
#
#
# @pytest.mark.anyio
# async def test_set_public_key_raise_user_not_found_error():
#     # Arrange
#     user_service = UserServiceStub()
#
#     user = UserV1ModelFaker().with_random_session().model
#     public_key = PublicKeyModelFaker(user.user_id).model
#
#     user_service.user_repo.get_safely.return_value = None
#
#     # Act, Assert
#     with pytest.raises(UserNotFoundError):
#         await user_service.set_publickey(user.user_id, user.hash_of_password, public_key)
#
#
# @pytest.mark.anyio
# async def test_set_public_key_raise_authentication_error():
#     # Arrange
#     user_service = UserServiceStub()
#
#     user = UserV1ModelFaker().with_random_session().model
#     public_key = PublicKeyModelFaker(user.user_id).model
#
#     user_service.publickey_repo.query.return_value = user.copy(update={'hash_of_password': ''})
#
#     # Act, Assert
#     with pytest.raises(AuthenticationError):
#         await user_service.set_publickey(user.user_id, user.hash_of_password, public_key)
