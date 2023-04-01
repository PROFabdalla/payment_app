from django.contrib import admin

from order.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_by",
        "order_no",
        "completed",
        "order_status",
    ]
    list_editable = [
        "completed",
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "product",
        "quantity",
    ]
