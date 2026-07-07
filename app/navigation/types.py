from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    template: str
    context: object = None
