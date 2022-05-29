from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post


@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f"https://www.pixiv.net/fanbox/creator/{user_id}"


@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f"https://www.pixiv.net/fanbox/creator/{user_id}/post/{post_id}"


@dataclass
class Fanbox(Paysite):
    name: str = 'fanbox'
    title: str = 'Pixiv Fanbox'
    user: User = User()
    post: Post = Post()
    color: str = '#2c333c'
