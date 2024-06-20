from src.domain.abstractions.repositories import IUserRepository
from src.domain.abstractions.services import ISearchService, IUserService
from src.domain.models import UserModel, SessionModel


class SearchService(ISearchService):

    def __init__(self,
                 user_service: IUserService,
                 user_repo: IUserRepository):
        self.__user_repo = user_repo
        self.__user_service = user_service

    async def user_search(self, session: SessionModel, search_string: str = None, **kwargs) -> list[UserModel | None]:
        search_result: list[UserModel] = []
        for user_id, user_entity in (await self.__user_repo.query_all()).items():
            user_entity_dict = user_entity.dict()
            if search_string is not None:
                if search_string.lower() in user_entity_dict.get('nickname').lower():
                    user_model = await self.__user_service.get_user(user_id, session)
                    search_result.append(user_model)
                elif len(search_string) >= 5 and search_string.lower() in user_entity_dict.get('user_id').lower():
                    user_model = await self.__user_service.get_user(user_id, session)
                    search_result.append(user_model)
            else:
                for arg, val in kwargs.items():
                    if isinstance(val, str):
                        if val.lower() in user_entity_dict.get(arg).lower():
                            user_model = await self.__user_service.get_user(user_id, session)
                            search_result.append(user_model)
                    elif isinstance(val, int):
                        if user_entity_dict.get(arg) == val:
                            user_model = await self.__user_service.get_user(user_id, session)
                            search_result.append(user_model)
        return search_result
