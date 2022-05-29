from abc import abstractmethod
from dataclasses import dataclass

from src.internals.types import AbstractDataclass


@dataclass
class Service_User(AbstractDataclass):
    """
    User-related info for a service.
    """
    @abstractmethod
    def profile(self, user_id: str) -> str:
        """A profile link for the service"""


@dataclass
class Service_Post(AbstractDataclass):
    """
    Post-related info for a service.
    """
    @abstractmethod
    def link(self, post_id: str, user_id: str) -> str:
        """
        A profile link for the service.
        Because fanbox requires `post_id` and `artist_id` for post link, all services will have to have 2 arguments for this method.
        """


@dataclass
class Paysite(AbstractDataclass):
    """
    Holds all info related to the paysite.
    """
    name: str
    title: str
    user: Service_User
    post: Service_Post
    color: str
