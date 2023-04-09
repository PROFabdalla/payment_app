from django.urls import path
from order.views import OrderView, OrderDetails, orders


urlpatterns = [
    path("api/", OrderView.as_view(), name="orders"),
    path("api/<int:pk>/", OrderDetails.as_view(), name="orders_details"),
    # --------------------- templates --------------------- #
    path("", orders, name="orders"),
]
