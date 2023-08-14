from datetime import datetime

from django.db.models import Q

from admin_actions.models import AdminAction
from admin_actions.serializers import AdminActionSerializer
from dateutil.relativedelta import relativedelta


def get_admin_actions(starts_at: datetime, ends_at: datetime) -> AdminActionSerializer:
    admin_actions = AdminAction.objects.filter(
        Q(created_at__gte=starts_at) & Q(created_at__lte=ends_at + relativedelta(days=1))
    ).order_by("-created_at")

    return AdminActionSerializer(admin_actions, many=True)
