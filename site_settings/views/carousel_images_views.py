from django.core.serializers import serialize

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from site_settings.services.carousel_images_services import *


@api_view(["GET"])
def get_carousel_images_view(_):
    carousel_images = get_carousel_images()
    return Response({"carousel_images": serialize("python", carousel_images)})


@api_view(["POST"])
@parser_classes([MultiPartParser])
def save_carousel_images_view(request):
    save_carousel_images(request.data, request.FILES)
    return Response({"success": True})
