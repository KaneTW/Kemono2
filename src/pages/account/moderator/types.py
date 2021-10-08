from typing import List, Dict

class Dashboard:
    def __init__(self) -> None:
        self.current_page = 'mod'

class Files:
    def __init__(self, files: List[Dict]) -> None:
        self.current_page = 'mod'
        self.files = files

class Moderator:
    def __init__(self) -> None:
        self.Dashboard = Dashboard
        self.Files = Files

mod_props = Moderator()
