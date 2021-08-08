from datetime import datetime
from typing import Optional

class DM:
    def __init__(self, 
        id: str,
        user: str,
        service: str,
        content: str,
        added: datetime,
        published: datetime,
        embed: dict,
        file: dict,
        contributor_id: str,
        import_id: Optional[str]
    ) -> None:
        self.id = id
        self.user = user
        self.service = service
        self.content = content
        self.added = added
        self.published = published
        self.embed = embed
        self.file = file
        self.contributor_id = contributor_id
        self.import_id = import_id 

# class __Post:
#     id: str
#     user: str
#     service: str
#     added: datetime
#     published: datetime
#     edited: datetime
#     file: dict
#     attachments: list[dict]
#     title: str
#     content: str
#     embed: dict
#     shared_file: bool
    
class User:
    def __init__(self,
        id: str,
        name: str,
        service: str,
        indexed: datetime,
        updated: datetime,
        count: Optional[int]
    ) -> None:
        self.id = id
        self.name = name
        self.service = service
        self.indexed = indexed
        self.updated = updated
        self.count = count if count else None
    
# class __Favorite_Post:
#     id: str
#     account_id: str
#     service: str
#     artist_id: str
#     post_id: str

# class __Favorite_User:
#     id: str
#     account_id: str
#     service: str
#     artist_id: str

# class __Request:
#     id: str
#     service: str
#     user: str
#     post_id: str
#     title: str
#     description: str
#     created: datetime
#     image: str
#     price: float
#     votes: int
#     ips: str
#     status: str

# class __Log:
#     log0: str
#     log: list[str]
#     created: datetime

class PageProps:
    def __init__(self, current_page: str) -> None:
        self.current_page = current_page

class Kemono_Types:
    def __init__(self) -> None:
        self.DM = DM
        # self.Post = __Post
        self.User = User
        # self.Request = __Request
        # self.Favourite_Post = __Favorite_Post
        # self.Favourite_User = __Favorite_User
        # self.Log = __Log
        self.PageProps = PageProps

kemono_types = Kemono_Types()
