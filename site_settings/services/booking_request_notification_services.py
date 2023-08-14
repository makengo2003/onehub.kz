from typing import Sequence

from django.db.models import QuerySet

from site_settings.models import BookingRequestNotificationEmail


def get_booking_request_notification_emails() -> QuerySet[int]:
    return BookingRequestNotificationEmail.objects.values_list("email", flat=True)


def save_booking_request_notification_emails(emails: Sequence[str]) -> None:
    orm_emails = list()

    for email in emails:
        if email:
            orm_emails.append(BookingRequestNotificationEmail(email=email))

    BookingRequestNotificationEmail.objects.all().delete()
    BookingRequestNotificationEmail.objects.bulk_create(orm_emails)
