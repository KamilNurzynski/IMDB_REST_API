from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    '''
    na stronie django rest api jest dużo więcej opcji
    '''

    page_size = 10
    # page_query_param = 'strona' # tutaj możemy pwisać inną nazwę parametru, który będzie używany w URL
    # poniższy parametr nadpisuje page_size. można np stronę paginwac co 100rekordów. Działa nie tylko dla pierwszej strony
    page_size_query_param = 'size'  # można w URL wpisać size=100 i mieć sto na jednej stronie.
    max_page_size = 6  # nawet jak ktoś wpisze size=1000 to mu się załaduje max 6 na stronę. WARTO DODAC
    # last_page_strings = 'ostatnia' #dafaultowo wpisując ?page=last dostajemy ostatnią stronę. tutaj nadpisujemy: ?strona=ostatnia


class WatchListWithLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5  # ile rekordów na per strona
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'startuje_od'  # offset to jest od którego elementu zaczynamy. Majac w bazie 50 rekordów, offset=13 to zaczynamy od elementu 13 albo 14.


class WatchListCursorPagination(CursorPagination):
    """
    Przykładem użycia moze być umowa z wieloma stronami, gdzie każda strana musi być wyświetlona
    """
    page_size = 5
    ordering = 'created' #pole w klasie models może być
    cursor_query_param = 'record' # wstawi w url zamiast cursor