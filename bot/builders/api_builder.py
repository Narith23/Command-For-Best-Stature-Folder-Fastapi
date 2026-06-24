"""API project file builder."""

from pathlib import Path

from bot.utils.file_writer import write_file


def create_api_files(project_path: Path) -> None:
    """Create API controllers, routes, models, requests, and tests."""

    write_file(
        project_path / "routes" / "api.py",
        '''"""API routes."""

from fastapi import APIRouter

from app.Http.Controllers.Api.health_controller import router as health_router
from app.Http.Controllers.Api.item_controller import router as item_router


router = APIRouter(prefix="/api/v1")
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(item_router, prefix="/items", tags=["items"])
''',
        overwrite=True,
    )
    write_file(
        project_path
        / "app"
        / "Http"
        / "Controllers"
        / "Api"
        / "health_controller.py",
        '''"""Health check controller."""

from pydantic import BaseModel, ConfigDict, Field
from fastapi import APIRouter

from vendor.helpers import ApiResponse, success_response


class HealthData(BaseModel):
    status: str = Field(json_schema_extra={"example": "ok"})

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
            }
        }
    )


router = APIRouter()


@router.get("", response_model=ApiResponse[HealthData])
def index():
    return success_response(
        message="API is running",
        data=HealthData(status="ok"),
    )
''',
        overwrite=True,
    )
    write_file(
        project_path
        / "app"
        / "Http"
        / "Controllers"
        / "Api"
        / "item_controller.py",
        '''"""Item API controller."""

from fastapi import APIRouter, status

from app.Http.Requests.item_request import StoreItemRequest
from app.Http.Resources.item_resource import ItemResource
from app.Services.item_service import ItemService
from vendor.helpers import ApiResponse, error_response, success_response


router = APIRouter()


@router.get("", response_model=ApiResponse[list[ItemResource]])
def index():
    items = ItemService.all()

    data = [
        ItemResource.from_model(item)
        for item in items
    ]

    return success_response(
        message="Items fetched successfully",
        data=data,
    )


@router.get("/{item_id}", response_model=ApiResponse[ItemResource])
def show(item_id: int):
    item = ItemService.find(item_id)

    if not item:
        return error_response(
            message="Item not found",
            errors={
                "code": "NOT_FOUND",
                "detail": "Item with this ID does not exist",
            },
        )

    return success_response(
        message="Item fetched successfully",
        data=ItemResource.from_model(item),
    )


@router.post(
    "",
    response_model=ApiResponse[ItemResource],
    status_code=status.HTTP_201_CREATED,
)
def store(payload: StoreItemRequest):
    item = ItemService.create(payload)

    return success_response(
        message="Item created successfully",
        data=ItemResource.from_model(item),
    )
''',
        overwrite=True,
    )
    write_file(
        project_path / "app" / "Http" / "Requests" / "item_request.py",
        '''"""Item request schemas."""

from pydantic import BaseModel, Field


class StoreItemRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
''',
        overwrite=True,
    )
    write_file(
        project_path / "app" / "Http" / "Resources" / "item_resource.py",
        '''"""Item response resources."""

from pydantic import BaseModel, ConfigDict, Field

from app.Models.item import Item


class ItemResource(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    name: str = Field(json_schema_extra={"example": "Sample Item"})
    description: str | None = Field(
        json_schema_extra={"example": "Laravel-style FastAPI item"},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Sample Item",
                "description": "Laravel-style FastAPI item",
            }
        }
    )

    @classmethod
    def from_model(cls, item: Item):
        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
        )
''',
        overwrite=True,
    )
    write_file(
        project_path / "app" / "Models" / "item.py",
        '''"""Item domain model."""

from dataclasses import dataclass


@dataclass
class Item:
    id: int
    name: str
    description: str | None = None
''',
        overwrite=True,
    )
    write_file(
        project_path / "app" / "Services" / "item_service.py",
        '''"""Item business logic."""

from app.Http.Requests.item_request import StoreItemRequest
from app.Models.item import Item


class ItemService:
    """Small in-memory item service for the generated starter app."""

    _items = [
        Item(id=1, name="Sample Item", description="Laravel-style FastAPI item"),
    ]
    _next_id = 2

    @classmethod
    def all(cls) -> list[Item]:
        return cls._items

    @classmethod
    def find(cls, item_id: int) -> Item | None:
        return next((item for item in cls._items if item.id == item_id), None)

    @classmethod
    def create(cls, payload: StoreItemRequest) -> Item:
        item = Item(
            id=cls._next_id,
            name=payload.name,
            description=payload.description,
        )
        cls._items.append(item)
        cls._next_id += 1

        return item
''',
        overwrite=True,
    )
    write_file(
        project_path / "tests" / "test_health.py",
        '''"""Health endpoint tests."""

from app.Http.Controllers.Api.health_controller import HealthData, index
from vendor.helpers.response import ApiResponse


def test_health_check():
    response = index()

    assert isinstance(response, ApiResponse)
    assert response.success is True
    assert response.message == "API is running"
    assert response.data == HealthData(status="ok")
''',
        overwrite=True,
    )
