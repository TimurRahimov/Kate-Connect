from fastapi import APIRouter

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import IUserService

router_people_api = APIRouter()


@router_people_api.get("/api/v1/people")
async def get_people(count: int = None):
    user_service = ServiceContainer.get(IUserService)
    return await user_service.get_people(count)

# @router_v1.post("api/v1/{user_id}/send-message")
# async def send_message(user_id: str,
#                        session: Annotated[str, Form()],
#                        text_enc_by_from: UploadFile,
#                        text_enc_by_to: UploadFile) -> dict:
#     session = SessionV1Model.parse_raw(session)
#     msg_service = ServiceContainer.get(IMessageService)
#     msg = MessageV1Model(user_to_id=user_id,
#                          text_enc_by_from=await text_enc_by_from.read(),
#                          text_enc_by_to=await text_enc_by_to.read(),
#                          session=session)
#     await msg_service.send_message(msg)
#     return {}
#
#
# @router_v1.post("/api/v1/get-chats")
# async def get_all_chats_bytes(session: SessionV1Model = Body(...)) -> Response:
#     # list[ChatV1]
#     msg_service = ServiceContainer.get(IMessageService)
#     chats = [c.dict() for c in await msg_service.get_all_chats(session)]
#     return Response(content=pickle.dumps(chats))
