# # -*- coding: utf-8 -*-
from django.contrib import admin

from user_payment.models import UserPayment


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "app_user",
        "payment_bool",
        "stripe_checkout_id",
    )
