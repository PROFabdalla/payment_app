from django.conf import settings
from rest_framework import serializers

from order.models import Order


class OrderCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ()
