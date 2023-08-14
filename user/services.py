import os
from threading import Thread
from typing import Mapping, Tuple, Union

from booking.models import BookingRequest
from site_settings.models import BookingRequestNotificationEmail
from .forms import LeaveBookingRequestForm

from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from project.settings import EMAIL_HOST_USER


def leave_booking_request(form_data: Mapping) -> Tuple[Union[BookingRequest, None], bool]:
    form = LeaveBookingRequestForm(form_data)
    if form.is_valid():
        return form.save(), True
    return None, False


class BookingRequestNotificationEmailMessage:
    def __init__(self, subject: str, content: str):
        self.subject: str = subject
        self.content: str = content
        # self.to: Iterable[str] = to

    def send(self) -> None:
        for email in BookingRequestNotificationEmail.objects.all():
            send_mail(self.subject, self.content, EMAIL_HOST_USER, [email], fail_silently=False, html_message=self.content)  # os.system(f'echo "{self.content}" | mail -s "{self.subject}\nContent-Type: text/html" {email}')


def notify_administrators_of_booking_request(booking_request: BookingRequest) -> None:
    message = BookingRequestNotificationEmailMessage(
        "OneHub.kz New Booking Request",
        f"""<b>New booking request:</b><br>
        From: {booking_request.consumer_fullname}<br>
        Phone: {booking_request.consumer_phone_number}<br>
        Place type: {booking_request.place_type}<br>
        Created at: {booking_request.created_at}<br>
        Don't forget to handle the request,<br>
        then save changes in <a href='onehub.kz/admin'>onehub.kz/admin</a>"""
    )
    Thread(target=message.send, daemon=True).start()


def user_login(request):
    form = AuthenticationForm(request, request.POST)

    if form.is_valid():
        auth_login(request, form.get_user())
        return True
    return False
