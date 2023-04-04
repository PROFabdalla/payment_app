from rest_flex_fields import FlexFieldsModelSerializer
from product.models import Product
from djmoney.contrib.django_rest_framework import MoneyField
from user_app.models import User


class ProductUserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class ProductSerializer(FlexFieldsModelSerializer):
    price = MoneyField(max_digits=5, decimal_places=2)

    class Meta:
        model = Product
        fields = (
            "id",
            "created_by",
            "title",
            "slug",
            "description",
            "image",
            "stock",
            "unit",
            "price",
            "country",
        )
        extra_kwargs = {
            "created_by": {"required": False, "read_only": True},
        }
        expandable_fields = {
            "created_by": (ProductUserSerializer, {"many": False}),
        }

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.update(created_by=user)
        return super().create(validated_data)
