from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post


@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return ''


@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return ''


@dataclass
class Afdian(Paysite):
    name: str = 'afdian'
    title: str = 'Afdian'
    user: User = User()
    post: Post = Post()
    color: str = '#9169df'
