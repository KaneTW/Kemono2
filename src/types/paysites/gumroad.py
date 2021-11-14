from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post

@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f"https://gumroad.com/{user_id}"

@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f"https://gumroad.com/l/{post_id}"

@dataclass
class Gumroad(Paysite):
    name: str = 'gumroad'
    title: str = 'Gumroad'
    user: User = User()
    post: Post = Post()
