from typing import List, Tuple

from fastapi_auth.filters import SearchFilter


class SqlAlchemySearchFilter(SearchFilter):
    async def _get_instance(self, field_names: List[str], instance: object) -> Tuple[str, object]:
        for i in range(len(field_names) - 1):
            instance = await getattr(instance.awaitable_attrs, field_names[i])
            if instance is None:
                return field_names[-1], None
        return field_names[-1], instance
