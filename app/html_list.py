from dataclasses import dataclass
from typing import Generic, List, TypeVar
from app.view import View

T = TypeVar("T")


@dataclass(frozen=True)
class HtmlList(Generic[T]):
    id: str
    style: str
    items: List[View[T]]
