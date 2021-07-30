from typing import Optional, List
from ..types.kemono import DM

class StatusPageProps:
    def __init__(self, 
        current_page: str,
        import_id: str,
        dms: Optional[List[DM]]
    ) -> None:
        self.current_page = current_page
        self.import_id = import_id
        self.dms = dms

class DMPageProps:
    def __init__(self, 
        current_page: str,
        import_id: str,
        account_id: str,
        dms: Optional[List[DM]]
    ) -> None:
        self.current_page = current_page
        self.import_id = import_id
        self.dms = dms
        self.account_id = account_id
