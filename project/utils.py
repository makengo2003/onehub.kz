from typing import Literal, Callable

from .settings import TIME_DIFFERENCE_BETWEEN_SERVER_AND_KZ
from datetime import datetime
from dateutil.relativedelta import relativedelta


def datetime_now() -> datetime:
    return datetime.now() + relativedelta(hours=TIME_DIFFERENCE_BETWEEN_SERVER_AND_KZ)


def request_schema_validation(request_method: Literal["GET", "POST"], schema) -> Callable:
    def decorator(function):
        def wrapper(*args, **kwargs):
            if request_method == "GET":
                request_data = args[0].query_params
            else:
                request_data = args[0].data

            serializer = schema(data=request_data)
            serializer.is_valid(raise_exception=True)

            if request_method == "GET":
                args[0].query_params._mutable = True
                args[0].query_params.update(serializer.validated_data)
            else:
                args[0].data.update(serializer.validated_data)

            return function(*args, **kwargs)
        return wrapper
    return decorator
