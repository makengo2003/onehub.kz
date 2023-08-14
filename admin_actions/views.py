from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from project.utils import request_schema_validation
from . import services, schemas


@api_view(["GET"])
@permission_classes([IsAdminUser])
@request_schema_validation("GET", schemas.GetAdminActionsRequestSchema)
def get_admin_actions_view(request: Request) -> Response:
    admin_actions = services.get_admin_actions(request.query_params.get("starts_at"),
                                               request.query_params.get("ends_at"))
    return Response(admin_actions.data)
