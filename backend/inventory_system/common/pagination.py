from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10      # default records
    max_limit = 100         # safety limit
    limit_query_param = "limit"
    offset_query_param = "offset"