from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.exceptions import RequestValidationError
from sqlmodel import SQLModel, select
from pydantic import create_model
from ..db import AsyncSession, get_session


class NotFoundException(HTTPException):
    def __init__(self, headers=None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
            headers=headers,
        )


def validate(Model: type[SQLModel], obj):
    try:
        return Model.model_validate(obj)
    except Exception as e:
        raise RequestValidationError(e)


def CRUDLRouter(Model: type[SQLModel]) -> APIRouter:
    Item = Model
    ItemUpdate = create_model(
        f"{Model.__name__}Update",
        **{field: (Optional[t], None) for field, t in Model.__annotations__.items()},
        __base__=SQLModel,
    )

    ItemMap = create_model(
        f"{Model.__name__}Map",
        __base__=Item,
        __cls_kwargs__={"table": True},
    )

    route = Item.__route__ or Item.__tablename__

    router = APIRouter(prefix=f"/{route}", tags=[route])

    @router.post(
        "/",
        response_model=Item,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_item(
        item: dict,
        session: AsyncSession = Depends(get_session),
    ) -> dict:
        item = validate(ItemMap, item)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    @router.get(
        "/",
        response_model=list[Item],
    )
    async def list_items(
        session: AsyncSession = Depends(get_session),
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
    ) -> list[dict]:
        result = await session.execute(select(ItemMap).offset(offset).limit(limit))
        return result.scalars().all()

    @router.get(
        "/{id}",
        response_model=Item,
    )
    async def read_item(
        id,
        session: AsyncSession = Depends(get_session),
    ):
        item = await session.get(ItemMap, id)
        if not item:
            raise NotFoundException()
        return item

    @router.put("/{id}", response_model=Item)
    async def update_item(
        id,
        item_update: dict,
        session: AsyncSession = Depends(get_session),
    ):
        item = await session.get(ItemMap, id)
        if not item:
            raise NotFoundException()
        item_update = validate(ItemUpdate, item_update)
        update_data = item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def delete_item(
        id,
        session: AsyncSession = Depends(get_session),
    ):
        item = await session.get(ItemMap, id)
        if not item:
            raise NotFoundException()
        await session.delete(item)
        await session.commit()

    return router
