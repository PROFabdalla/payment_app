from rest_flex_fields import FlexFieldsModelSerializer
from order.models import OrderItem


class OrderItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "quantity",
        )
