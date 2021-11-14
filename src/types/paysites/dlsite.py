from dataclasses import dataclass
from .base import Paysite, Service_User, Service_Post

@dataclass
class User(Service_User):
    def profile(self, user_id: str) -> str:
        return f"https://www.dlsite.com/eng/circle/profile/=/maker_id/{user_id}"

@dataclass
class Post(Service_Post):
    def link(self, post_id: str, user_id: str) -> str:
        return f"https://www.dlsite.com/ecchi-eng/work/=/product_id/{post_id}"

@dataclass
class DLSite(Paysite):
    name: str = 'dlsite'
    title: str = 'DLsite'
    user: User = User()
    post: Post = Post()
