from rest_framework import serializers


class GetAdminActionsRequestSchema(serializers.Serializer):
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()

    def validate(self, attrs):
        if attrs["starts_at"] > attrs["ends_at"]:
            raise serializers.ValidationError({"ends_at": "Дата окончания должна быть больше даты начала"})
        return attrs
