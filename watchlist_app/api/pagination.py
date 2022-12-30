from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 10

    page_size_query_param = 'size'
    max_page_size = 6


class WatchListWithLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'startuje_od'


class WatchListCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'
