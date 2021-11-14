from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post


@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f"https://fantia.jp/fanclubs/{user_id}"


@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f"https://fantia.jp/posts/{post_id}"


@dataclass
class Fantia(Paysite):
    name: str = 'fantia'
    title: str = 'Fantia'
    user: User = User()
    post: Post = Post()
