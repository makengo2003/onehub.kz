from rest_framework.decorators import api_view
from rest_framework.response import Response

from resident.services import resident_services


@api_view(["GET"])
def calculate_resident_adding_price_view(request):
    success, status_code, message, price = resident_services.calculate_resident_adding_price(request.query_params)
    return Response({"success": success, "message": message, "price": price}, status=status_code)


@api_view(["POST"])
def add_resident_view(request):
    success, status_code, message = resident_services.add_resident(request.data)
    return Response({"success": success, "message": message}, status=status_code)


@api_view(["GET"])
def calculate_resident_renewing_price_view(request):
    success, status_code, message, price = resident_services.calculate_resident_renewing_price(request.query_params)
    return Response({"success": success, "message": message, "price": price}, status=status_code)


@api_view(["POST"])
def renew_resident_view(request):
    success, status_code, message = resident_services.renew_resident(request.data)
    return Response({"success": success, "message": message}, status=status_code)


@api_view(["POST"])
def delete_resident_view(request):
    resident_id = request.data.get("resident_id")
    resident_services.delete_resident(resident_id)
    return Response({"success": True})


@api_view(["POST"])
def update_resident_info_view(request):
    resident_id = request.data.get("resident_id")
    field_for_updating = request.data.get("field_for_updating")
    new_value = request.data.get("new_value")
    resident_services.update_resident_info(resident_id, field_for_updating, new_value)
    return Response({"success": True})


@api_view(["POST"])
def update_resident_visited_today_status_view(request):
    resident_id = request.data.get("resident_id")
    resident_services.update_resident_visited_today_status(resident_id)
    return Response({"success": True})


@api_view(["GET"])
def get_attendance_of_resident_view(request):
    attendance_of_resident = resident_services.get_attendance_of_resident(request.query_params.get("resident_id"))
    return Response({"attendance_of_resident": attendance_of_resident})


@api_view(["GET"])
def search_by_fullname_view(request):
    fullname = request.query_params.get("fullname")
    phone_number, profession = resident_services.search_by_fullname(fullname)
    return Response({"phone_number": phone_number, "profession": profession})


@api_view(["GET"])
def search_by_phone_number_view(request):
    phone_number = request.query_params.get("phone_number")
    fullname, profession = resident_services.search_by_phone_number(phone_number)
    return Response({"fullname": fullname, "profession": profession})
