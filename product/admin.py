from django.contrib import admin

from product.models import Product


@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_by",
        "title",
        "price",
        "slug",
        "stock",
        "unit",
        "country",
    ]
    list_editable = ["stock", "unit"]
