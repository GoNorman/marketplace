from fastapi import APIRouter, Depends, Request, UploadFile, BackgroundTasks
from ..security.security_config import security
from ..service.items_service import Item
from sqlalchemy.ext.asyncio import AsyncSession
from ..engine_database.database import get_async_session_factory

item_router = APIRouter(
    prefix="/items"
)

@item_router.get("/all_items")
async def get_all(session: AsyncSession = Depends(get_async_session_factory)):
    return await Item.get_all_items(session)

@item_router.post("/add_item", dependencies=[Depends(security.access_token_required)])
async def add_new_item_service(req: Request, title_: str, description_: str, price_: int, city_: str, files: list[UploadFile], bg: BackgroundTasks,
                               session: AsyncSession = Depends(get_async_session_factory)):
    return await Item.add_new_item(req, title_, description_, price_, city_, files, bg, session)

@item_router.get("/get_item/{id}")
async def get_current_item(id_: int, session: AsyncSession = Depends(get_async_session_factory)):
    return await Item.get_current_item(id_, session)

@item_router.post("/delete_item/{item}", dependencies=[Depends(security.access_token_required)])
async def delete_item(id_: int, urls_: list[str], session: AsyncSession = Depends(get_async_session_factory)):
    return await Item.delete_item(id_, urls_, session)
