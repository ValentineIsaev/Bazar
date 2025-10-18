class CatalogMenuService:
    def __init__(self, catalogs: tuple, page_capacity: int):
        self._page = 0
        self._catalogs = catalogs

        self._page_capacity = page_capacity

    @property
    def is_end_page(self) -> bool:
        return (self._page+1) * self._page_capacity >= len(self._catalogs)

    @property
    def is_start_page(self) -> bool:
        return self._page == 0

    def next_page(self):
        if not self.is_end_page:
            self._page += 1

    def back_page(self):
        if self._page > 0:
            self._page -= 1

    def get_catalogs(self) -> tuple:
        start_index = self._page * self._page_capacity
        end_index = min(start_index + self._page_capacity, len(self._catalogs))

        return self._catalogs[start_index:end_index]