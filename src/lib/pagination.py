import math

from flask import Request, url_for

from ..utils.utils import limit_int, parse_int

class Pagination:
    def __init__(self, request: Request) -> None:
        self.current_page = parse_int(request.args.get('page'), 1)
        self.limit = limit_int(int(request.args.get('limit') or 25), 25)
        self.offset = self.calculate_offset(self.current_page, self.limit)
        self.base = request.args.to_dict()
        
        self.base.pop('page', None)

        self.count = None
        self.current_count = None
        self.total_pages = None
    
    def add_count(self, count: int):
        self.count = count
        self.current_count = self.offset + self.limit if self.offset + self.limit < self.count else self.count
        self.total_pages = math.ceil(self.count / self.limit) or 1

    def calculate_offset(self, current_page: int, limit: int):
        offset = None
        if current_page > 1:
            offset = (current_page - 1) * limit
        else:
            offset = 0

        return offset

    def create_paged_url(self, request: Request, page_number: int):
        url = url_for(request.endpoint, page = page_number, **self.base)

        return url
