from fastapi_auth.pagination import LimitOffsetPagination


class DefaultLimitOffsetPagination(LimitOffsetPagination):
    DEFAULT_LIMIT = 100
