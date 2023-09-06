from typing import Tuple, Mapping, Optional, Sequence

from dateutil.relativedelta import relativedelta
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import QuerySet, Q, Max, F
from rest_framework import serializers
from rest_framework.request import Request

from booking.models import BookedPlace, BookingRequest, RejectedBookingRequest, AcceptedBookingRequest
from project import settings
from project.utils import datetime_now
from datetime import datetime
from resident.models import Resident, ResidentVisitedDay

import pandas as pd


class ChangeUsernameAndPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    old_password = serializers.CharField(max_length=50)
    new_password1 = serializers.CharField(max_length=50)
    new_password2 = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ["username", "old_password", "new_password1", "new_password2"]

    def validate_old_password(self, old_password: str) -> str:
        if self.instance:
            if not self.instance.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Старый пароль неверный"})
        return old_password

    def validate_username(self, username: str) -> str:
        request_user = getattr(settings, 'request_user', None)
        user_already_exists = User.objects.filter(username=username).exists()

        if user_already_exists and request_user.username != username:
            raise serializers.ValidationError({"username": "Пользователь с таким именем уже существует"})

        return username

    def validate(self, attrs: Mapping) -> Mapping:
        if attrs["new_password1"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password2": "Указанные пароли не совпадают"})
        elif attrs["new_password1"] == attrs["old_password"]:
            raise serializers.ValidationError({"new_password1": "Новый пароль совпадает со старым паролем"})
        return attrs

    def update(self, user: User, validated_data: Mapping) -> User:
        user.username = validated_data.get("username")
        user.set_password(validated_data.get("new_password1"))
        user.save(update_fields=["password", "username"])
        return user


def change_username_and_password(request: Request, user: User, data: Mapping) -> None:
    serializer = ChangeUsernameAndPasswordSerializer(user, data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    auth_login(request, user)


def get_booked_places_list(last_obj_id: Optional[int] = 0) -> Tuple[QuerySet[BookedPlace], int]:
    booked_places_list = BookedPlace.objects.filter(status__in=["active", "expired"], id__gt=last_obj_id).order_by("-id")
    return booked_places_list, booked_places_list.aggregate(Max('id'))["id__max"]


def get_deleted_booked_places_list(last_obj_id: Optional[int], starts_at: datetime, ends_at: datetime) -> Tuple[QuerySet[BookedPlace], int]:
    deleted_booked_places_list = BookedPlace.objects.filter(status="deleted", deleted_at__gte=starts_at,
                                                            deleted_at__lt=ends_at).order_by("deleted_at")
    return deleted_booked_places_list, deleted_booked_places_list.aggregate(Max('id'))["id__max"]


def get_booking_requests_list(last_obj_id: Optional[int] = 0) -> Tuple[QuerySet[BookingRequest], int]:
    booking_requests_list = BookingRequest.objects.filter(id__gt=last_obj_id).annotate(
        rejection_reason=F('rejected_booking_request__rejection_reason')
    ).order_by("-id")
    return booking_requests_list, booking_requests_list.aggregate(Max('id'))["id__max"]


def get_residents_list(last_obj_id: Optional[int] = 0) -> Tuple[Sequence, int]:
    residents_list = Resident.objects.filter(status__in=["active", "expired"], id__gt=last_obj_id).order_by("-id")
    visited_today = ResidentVisitedDay.objects.filter(date=datetime_now().date()).values_list("resident_id", flat=True)
    serialized = serialize("python", residents_list)

    for i in serialized:
        i["fields"]["visited_today"] = i["pk"] in visited_today

    return serialized, residents_list.aggregate(Max('id'))["id__max"]


def get_deleted_residents_list(last_obj_id: Optional[int], starts_at: datetime, ends_at: datetime) -> Tuple[QuerySet[Resident], int]:
    deleted_residents_list = Resident.objects.filter(status="deleted", deleted_at__gte=starts_at,
                                                     deleted_at__lt=ends_at).order_by("deleted_at")
    return deleted_residents_list, deleted_residents_list.aggregate(Max('id'))["id__max"]


def export_to_excel(given_datetime__gte: datetime, file_name: str) -> str:
    now = datetime_now()

    df1_columns = [
        "ID",
        "Consumer fullname",
        "Consumer phone number",
        "Place type",
        "Created at",
        "Answered at",
        "Rejection Reason",
    ]
    rows1 = []
    for rejected_booking_request in RejectedBookingRequest.objects.filter(
            created_at__gte=given_datetime__gte).select_related("booking_request"):
        rows1.append([rejected_booking_request.id,
                      rejected_booking_request.booking_request.consumer_fullname,
                      rejected_booking_request.booking_request.consumer_phone_number,
                      rejected_booking_request.booking_request.place_type,
                      rejected_booking_request.booking_request.created_at,
                      rejected_booking_request.booking_request.answered_at,
                      rejected_booking_request.rejection_reason])

    df1 = pd.DataFrame(rows1, index=[f'row {i}' for i in range(1, len(rows1) + 1)],
                       columns=df1_columns)

    df2_columns = [
        "ID",
        "Consumer fullname",
        "Consumer phone number",
        "Place type",
        "Created at",
        "Answered at",
        "Booked Place ID",
    ]
    rows2 = []
    for accepted_booking_request in AcceptedBookingRequest.objects.filter(
            created_at__gte=given_datetime__gte).select_related("booking_request"):
        rows2.append([accepted_booking_request.id,
                      accepted_booking_request.booking_request.consumer_fullname,
                      accepted_booking_request.booking_request.consumer_phone_number,
                      accepted_booking_request.booking_request.place_type,
                      accepted_booking_request.booking_request.created_at,
                      accepted_booking_request.booking_request.answered_at,
                      accepted_booking_request.booked_place_id])

    df2 = pd.DataFrame(rows2, index=[f'row {i}' for i in range(1, len(rows2) + 1)],
                       columns=df2_columns)

    df3_columns = [
        "ID",
        "Consumer fullname",
        "Consumer phone number",
        "Booking period starts at",
        "Booking period expires at",
        "Deleted at",
        "Created at",
        "Status",
        "Deposit",
        "Deposit Is Paid",
        "Payment Type",
        "Place Number",
        "Place Type",
        "Duration",
        "Term",
        "Time type",
    ]
    rows3 = BookedPlace.objects.filter(
        created_at__gte=given_datetime__gte).values_list("id",
                                                        "consumer_fullname",
                                                        "consumer_phone_number",
                                                        "starts_at",
                                                        "expires_at",
                                                        "deleted_at",
                                                        "created_at",
                                                        "status",
                                                        "deposit",
                                                        "is_paid",
                                                        "payment_type",
                                                        "number",
                                                        "type",
                                                        "duration",
                                                        "term",
                                                        "time_type",
                                                        )
    df3 = pd.DataFrame(rows3,
                       index=[f'row {i}' for i in range(1, len(rows3) + 1)], columns=df3_columns)

    df4_columns = [
        "ID",
        "Date",
        "Resident ID",
    ]
    rows4 = ResidentVisitedDay.objects.filter(date__gte=given_datetime__gte).values_list("id", "date",
                                                                                                   "resident")
    df4 = pd.DataFrame(rows4, index=[f'row {i}' for i in range(1, len(rows4) + 1)], columns=df4_columns)

    df5_columns = [
        "ID",
        "Fullname",
        "Phone number",
        "Profession",
        "Booking period starts at",
        "Booking period expires at",
        "Deleted at",
        "Created at",
        "Status",
        "Used Discount",
        "Price",
        "Payment Type",
        "Place Number",
        "Place Type",
        "Paper Count",
        "Duration",
        "Term",
        "Time type",
    ]
    rows5 = Resident.objects.filter(
        created_at__gte=given_datetime__gte).values_list("id",
                                                        "fullname",
                                                        "phone_number",
                                                        "profession",
                                                        "starts_at",
                                                        "expires_at",
                                                        "deleted_at",
                                                        "created_at",
                                                        "status",
                                                        "used_discount",
                                                        "price",
                                                        "payment_type",
                                                        "place_number",
                                                        "place_type",
                                                        "paper_count",
                                                        "duration",
                                                        "term",
                                                        "time_type",
                                                        )
    df5 = pd.DataFrame(rows5,
                       index=[f'row {i}' for i in range(1, len(rows5) + 1)], columns=df5_columns)

    with pd.ExcelWriter(file_name) as writer:
        df1["Created at"] = pd.to_datetime(df1["Created at"], errors='coerce')
        df1["Answered at"] = pd.to_datetime(df1["Answered at"], errors='coerce')
        df2["Created at"] = pd.to_datetime(df2["Created at"], errors='coerce')
        df2["Answered at"] = pd.to_datetime(df2["Answered at"], errors='coerce')
        df3["Deleted at"] = pd.to_datetime(df3["Deleted at"], errors='coerce')
        df3["Created at"] = pd.to_datetime(df3["Created at"], errors='coerce')
        df5["Deleted at"] = pd.to_datetime(df5["Deleted at"], errors='coerce')
        df5["Created at"] = pd.to_datetime(df5["Created at"], errors='coerce')
        df3["Booking period expires at"] = pd.to_datetime(df3["Booking period expires at"], errors='coerce')
        df3["Booking period starts at"] = pd.to_datetime(df3["Booking period starts at"], errors='coerce')
        df5["Booking period expires at"] = pd.to_datetime(df5["Booking period expires at"], errors='coerce')
        df5["Booking period starts at"] = pd.to_datetime(df5["Booking period starts at"], errors='coerce')

        df1["Created at"] = df1['Created at'].dt.tz_localize(None)
        df1["Answered at"] = df1["Answered at"].dt.tz_localize(None)

        df2["Created at"] = df2["Created at"].dt.tz_localize(None)
        df2["Answered at"] = df2["Answered at"].dt.tz_localize(None)

        df3["Booking period expires at"] = df3["Booking period expires at"].dt.tz_localize(None)
        df3["Booking period starts at"] = df3["Booking period starts at"].dt.tz_localize(None)
        df3["Deleted at"] = df3["Deleted at"].dt.tz_localize(None)
        df3["Created at"] = df3["Created at"].dt.tz_localize(None)

        df5["Booking period expires at"] = df5["Booking period expires at"].dt.tz_localize(None)
        df5["Booking period starts at"] = df5["Booking period starts at"].dt.tz_localize(None)
        df5["Deleted at"] = df5["Deleted at"].dt.tz_localize(None)
        df5["Created at"] = df5["Created at"].dt.tz_localize(None)

        df1.to_excel(writer, sheet_name='Rejected Booking Requests')
        df2.to_excel(writer, sheet_name='Accepted Booking Requests')
        df3.to_excel(writer, sheet_name='Booked Places')
        df4.to_excel(writer, sheet_name='Resident Visited Days')
        df5.to_excel(writer, sheet_name='Residents')

        dataframes = {
            "Rejected Booking Requests": df1,
            "Accepted Booking Requests": df2,
            "Booked Places": df3,
            "Resident Visited Days": df4,
            "Residents": df5,
        }

        for sheet in dataframes.keys():
            worksheet = writer.sheets[sheet]
            df = dataframes[sheet]

            for idx, col in enumerate(df):  # loop through all columns
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),  # len of largest item
                    len(str(series.name))  # len of column name/header
                )) + 1  # adding a little extra space
                worksheet.set_column(idx, idx, max_len)  # set column width

    return file_name


def export_to_excel_2months() -> str:
    return export_to_excel(datetime_now() - relativedelta(months=2), "2months_report.xlsx")


def export_to_excel_daily() -> str:
    return export_to_excel(datetime_now() - relativedelta(hours=24), "daily_report.xlsx")
