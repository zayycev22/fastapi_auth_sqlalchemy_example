import datetime

from fastapi_auth import serializers


class UserSerializer(serializers.Serializer):
    email: str
    time_created: datetime.datetime
