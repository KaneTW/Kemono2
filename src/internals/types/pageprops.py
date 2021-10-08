from abc import abstractmethod
from dataclasses import dataclass, field

from src.internals.types import AbstractDataclass

@dataclass(init=False)
class PageProps(AbstractDataclass):
    """Base class for page `props`."""
    # currentPage: str
    # title: str
