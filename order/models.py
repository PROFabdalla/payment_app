from django.db import models
from user_app.models import User
from django.core.validators import MinValueValidator


class order_status(models.TextChoices):
    PLACED = "Placed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    RETURNED = "Return"
    FAILED = "Failed"


class Order(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order", verbose_name="order"
    )
    order_no = models.CharField(max_length=100, unique=True)
    completed = models.BooleanField(default=False)
    order_status = models.CharField(
        max_length=20,
        choices=order_status.choices,
        default=order_status.PLACED,
    )

    def total_price(self):
        items = self.items.all()
        total = sum([item.product.price.amount * item.quantity for item in items])
        return float(total) or 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        "product.Product", related_name="items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
