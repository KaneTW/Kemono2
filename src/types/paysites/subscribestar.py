from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post

@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f"https://subscribestar.adult/{user_id}"

@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f"https://subscribestar.adult/posts/{post_id}"

@dataclass
class Subscribestar(Paysite):
    name: str = 'subscribestar'
    title: str = 'SubscribeStar'
    user: User = User()
    post: Post = Post()
