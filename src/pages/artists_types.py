from typing import Callable, Dict, List

from ..types.kemono import DM, User, PageProps

class ArtistPageProps(PageProps):
    """
    TODO: remove `name` property.
    """
    def __init__(self,
        id: str,
        service: str,
        session: dict,
        name: str,
        count: int,
        limit: int,
        favorited: bool,
        artist: User,
        display_data: Callable[[dict], Dict[str, str]],
        dm_count: int
    ) -> None:
        super().__init__("posts")
        self.id = id 
        self.service = service 
        self.session = session 
        self.name = name 
        self.count = count 
        self.limit = limit 
        self.favorited = favorited 
        self.artist = artist 
        self.display_data = display_data
        self.dm_count = dm_count

class ArtistDMsProps(PageProps):
    def __init__(self,
        id: str,
        service: str,
        session: dict,
        artist: User,
        display_data: Callable[[dict], Dict[str, str]],
        dms: List[DM]
    ) -> None:
        super().__init__("dms")
        self.id = id 
        self.service = service 
        self.session = session 
        self.artist = artist 
        self.display_data = display_data
        self.dms = dms
