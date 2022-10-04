from drf_yasg import openapi

# keys ===============
AUTHORIZATION = 'authorization'
REQUEST = 'request'
SUCCESS = 'success'
ERROR = 'error'
MESSAGE = 'message'
DATA = 'data'

PAGE_INFO = 'page_info'
PAGE_TOTAL = 'page_total'
PAGE_COUNT = 'page_count'
PAGE_NUMBER = 'page_number'
TOTAL_COUNT = 'total_count'

ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'

USER = 'user'
USER_ID = 'user_id'

EMAIL = 'email'
MOBILE = 'mobile'
PASSWORD = 'password'
NEW_PASSWORD = 'new_password'

SEARCH = 'search'
DATE = 'date'


# header ===============
HEADER_TOKEN = openapi.Parameter(
    AUTHORIZATION,
    openapi.IN_HEADER,
    description='Bearer ex-eyJ0eXAiOiJKV1QiLCJhbGci......',
    type=openapi.TYPE_STRING,
    required=True
)

# query =================
QUERY_PARAM_PAGE_NUMBER = openapi.Parameter(
    PAGE_NUMBER,
    openapi.IN_QUERY,
    description='EX- 2',
    type=openapi.TYPE_INTEGER,
    required=False
)

QUERY_PARAM_PAGE_COUNT = openapi.Parameter(
    PAGE_COUNT,
    openapi.IN_QUERY,
    description='Number of element to be displayed on a page. ex-10',
    type=openapi.TYPE_INTEGER,
    required=False
)

QUERY_PARAM_SEARCH = openapi.Parameter(
    SEARCH,
    openapi.IN_QUERY,
    description='Search by...',
    type=openapi.TYPE_STRING,
    required=False
)

QUERY_PARAM_FILTER_BY_DATE = openapi.Parameter(
    DATE,
    openapi.IN_QUERY,
    description='Filter by date.',
    type=openapi.TYPE_STRING,
    required=False
)

QUERY_PARAM_USER_ID = openapi.Parameter(
    USER_ID,
    openapi.IN_QUERY,
    description='Ex-12',
    type=openapi.TYPE_INTEGER,
    required=True
)
