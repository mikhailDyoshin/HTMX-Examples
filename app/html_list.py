from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ListItems(Generic[T]):
    data: T
    template: str


@dataclass(frozen=True)
class HtmlList(Generic[T]):
    id: str
    style: str
    items: List[ListItems[T]]
