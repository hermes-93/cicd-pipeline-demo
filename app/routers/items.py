"""
Items CRUD router — a realistic domain model to demonstrate
request validation, error handling, and response schemas.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/items", tags=["items"])

# In-memory store; in production this would be a database
_db: dict[int, dict] = {}
_next_id: int = 1


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Widget"])
    description: str = Field(default="", max_length=500)
    price: float = Field(..., gt=0, examples=[9.99])


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float | None = Field(default=None, gt=0)


@router.get("/", response_model=list[ItemResponse], summary="List all items")
def list_items() -> list[dict]:
    return list(_db.values())


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item",
)
def create_item(payload: ItemCreate) -> dict:
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    _db[_next_id] = item
    _next_id += 1
    return item


@router.get("/{item_id}", response_model=ItemResponse, summary="Get item by ID")
def get_item(item_id: int) -> dict:
    item = _db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


@router.patch("/{item_id}", response_model=ItemResponse, summary="Partially update an item")
def update_item(item_id: int, payload: ItemUpdate) -> dict:
    item = _db.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    updates = payload.model_dump(exclude_none=True)
    item.update(updates)
    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
def delete_item(item_id: int) -> None:
    if item_id not in _db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    del _db[item_id]
