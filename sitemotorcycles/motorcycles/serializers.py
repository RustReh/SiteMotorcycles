from rest_framework import serializers

from .models import Motorcycles


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycles
        fields = "__all__"