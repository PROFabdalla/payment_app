from django.urls import path

from order.views import OrderDetails, OrderView, orders

urlpatterns = [
    path("api/", OrderView.as_view(), name="orders"),
    path("api/<int:pk>/", OrderDetails.as_view(), name="orders_details"),
    # --------------------- templates for test--------------------- #
    path("", orders, name="orders"),
]
