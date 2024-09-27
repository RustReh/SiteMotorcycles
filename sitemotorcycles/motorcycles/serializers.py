from rest_framework import serializers

from .models import Motorcycles, Order


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motorcycles
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
