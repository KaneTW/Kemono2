from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post

@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f"https://www.patreon.com/user?u={user_id}"

@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f"https://www.patreon.com/posts/{post_id}"

@dataclass
class Patreon(Paysite):
    name: str = 'patreon'
    user: User = User()
    post: Post = Post()
    title: str = 'Patreon'
