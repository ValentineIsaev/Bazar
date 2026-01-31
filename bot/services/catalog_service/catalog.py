from typing import Any, Callable


class CatalogMenuService:
    def __init__(self, catalogs: tuple[tuple[int, Any], ...], page_capacity: int):
        self._page = 0
        self._catalogs = catalogs

        self._page_capacity = page_capacity

        self._filters: dict[str, Callable] = {}
        self._filter_story: dict[str, dict] = {}
        self._raw_catalogs: tuple[tuple[int, Any], ...] = catalogs

    @property
    def is_end_page(self) -> bool:
        return (self._page+1) * self._page_capacity >= len(self._catalogs)

    @property
    def is_start_page(self) -> bool:
        return self._page == 0

    def get_all(self) -> tuple[tuple[int, Any] , ...]:
        return self._catalogs

    def next_page(self):
        if not self.is_end_page:
            self._page += 1

    def back_page(self):
        if self._page > 0:
            self._page -= 1

    def get_element_by_id(self, id_element: int) -> Any:
        index = next(i for i, j in enumerate(self._catalogs) if j[0] == id_element)
        return self._catalogs[index][1]

    def get_page_catalogs(self) -> tuple:
        start_index = self._page * self._page_capacity
        end_index = min(start_index + self._page_capacity, len(self._catalogs))

        return self._catalogs[start_index:end_index]

    def reset_filter(self):
        self._catalogs = self._raw_catalogs
        self._filters = {}
        self._filter_story = {}

    def set_filters(self, filters: dict[str, Callable[[tuple[int, Any], dict], bool]]):
        self._filters = filters

    def _processing_filter(self, filter_name: str, **filter_data):
        filter_ = self._filters.get(filter_name)
        self._catalogs = tuple(data for data in self._catalogs if filter_(data, **filter_data))

    def filter_catalog(self, filter_name, **filter_data):
        if not filter_name in self._filters:
            raise ValueError(f'The filter {filter_name} does not exist!')

        if (filter_name in self._filter_story and tuple(self._filter_story.keys())[-1] != filter_name or
                len(tuple(self._filter_story.keys())) == 1):
            del self._filter_story[filter_name]
            self._catalogs = self._raw_catalogs
            for name, data in self._filter_story.items():
                self._processing_filter(name, **data)

        self._filter_story[filter_name] = filter_data
        self._processing_filter(filter_name, **filter_data)

    def get_raw_catalog(self) -> tuple[tuple[int, Any], ...]:
        return self._raw_catalogs

    @property
    def is_set_filters(self) -> bool:
        return bool(self._filters)