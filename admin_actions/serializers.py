from rest_framework import serializers
from .models import AdminAction


class AdminActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAction
        fields = "__all__"
