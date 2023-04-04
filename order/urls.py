from django.urls import path
from order.views import OrderView, OrderDetails


urlpatterns = [
    path("", OrderView.as_view(), name="orders"),
    path("<int:pk>/", OrderDetails.as_view(), name="orders_details"),
]
