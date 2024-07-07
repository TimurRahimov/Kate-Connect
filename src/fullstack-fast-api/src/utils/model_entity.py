from src.domain.entities import UserEntity
from src.domain.models import UserModel, FriendModel, SessionModel
from src.utils.time import iso_time, time_iso


def user_m2e(user_model: UserModel, login: str) -> UserEntity:
    return UserEntity(
        user_id=user_model.user_id,
        login=login,
        nickname=user_model.nickname,
        avatar_link=user_model.avatar_link,
        last_time_online=time_iso(user_model.last_time_online),
    )


def user_e2m(user_entity: UserEntity,
             session: SessionModel = None,
             friends: list[FriendModel] = None,
             online: bool = False) -> UserModel:
    return UserModel(
        user_id=user_entity.user_id,
        nickname=user_entity.nickname,
        avatar_link=user_entity.avatar_link,
        session=session,
        last_time_online=iso_time(user_entity.last_time_online),
        friends=friends,
        online=online)
