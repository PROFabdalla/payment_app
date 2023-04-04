from rest_flex_fields import FlexFieldsModelSerializer
from order.models import Order, OrderItem
from order.serializers.order_relations import OrderItemSerializer


class OrderSerializer(FlexFieldsModelSerializer):
    items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_by",
            "order_no",
            "items",
            "completed",
            "order_status",
        )
        extra_kwargs = {
            "created_by": {"required": False, "read_only": True},
            "completed": {"required": False, "read_only": True},
            "order_status": {"required": False, "read_only": True},
            "order_no": {"required": False, "read_only": True},
        }
        # expandable_fields = {
        #     "created_by": (ProductUserSerializer, {"many": False}),
        # }

    def create(self, validated_data):
        items = validated_data.pop("items")
        user = self.context["request"].user

        # -------------------- order number -------------------- #
        quantity = sum([item["quantity"] for item in items])
        last_order = (Order.objects.last().id + 1) if Order.objects.last() else 1
        order_no = f"{user.name[:3].upper()}{str(quantity).zfill(3)}{str(user.pk)}{str(last_order)}"

        validated_data.update(created_by=user, order_no=order_no)
        order = super().create(validated_data)

        # -------------------- order item creation ------------------ #
        for item in items:
            order_item = OrderItem.objects.create(order=order, **item)
            order_item.product.stock -= item["quantity"]
            order_item.product.save()
        return order
