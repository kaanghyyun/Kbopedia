from django.http import HttpResponse

from .abstract_response import AbstractResponse
from ..exceptions.type_exceptions import NotAbstractModelError
from .obj.abstract_model import AbstractModel


class ModelResponse(AbstractResponse):
    @staticmethod
    def response(data: AbstractModel, status_code: int = 200) -> HttpResponse:
        if isinstance(data, AbstractModel):
            response = HttpResponse(data.toJson())
        else:
            raise NotAbstractModelError(f"{type(data)} is not an instance of AbstractModel.")
        response.status_code = status_code

        return response