# @api_view(["POST"])
# TODO: def add_residents_locker_view(request):
#     success, status_code, message = resident_services.add_residents_locker(request.data)
#     return Response({"success": success, "message": message}, status=status_code)
#
#
# @api_view(["POST"])
# TODO: def renew_residents_locker_view(request):
#     success, status_code, message = resident_services.renew_residents_locker(request.data)
#     return Response({"success": success, "message": message}, status=status_code)
#
#
# @api_view(["POST"])
# TODO: def delete_residents_locker_view(request):
#     residents_locker_id = request.data.get("residents_locker_id")
#     resident_services.delete_residents_locker(residents_locker_id)
#     return Response({"success": True})
#
#
# @api_view(["POST"])
# TODO: def update_residents_locker_info_view(request):
#     residents_locker_id = request.data.get("residents_locker_id")
#     field_for_updating = request.data.get("field_for_updating")
#     new_value = request.data.get("new_value")
#     resident_services.update_residents_locker_info(residents_locker_id, field_for_updating, new_value)
#     return Response({"success": True})
