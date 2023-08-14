from django.core.serializers import serialize

from rest_framework.decorators import api_view
from rest_framework.response import Response

from site_settings.services.booking_request_notification_services import *


@api_view(["GET"])
def get_booking_request_notification_emails_view(_):
    booking_request_notification_emails = get_booking_request_notification_emails()
    return Response({"booking_request_notification_emails": booking_request_notification_emails})


@api_view(["POST"])
def save_booking_request_notification_emails_view(request):
    save_booking_request_notification_emails(request.data.get("emails"))
    return Response({"success": True})
