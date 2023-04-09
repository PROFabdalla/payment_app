from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from order.models import Order
from order.serializers.order import OrderSerializer
from django.shortcuts import render


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(created_by=user)
        return queryset


class OrderDetails(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(created_by=user)
        return queryset


def orders(request):
    orders = Order.objects.filter(created_by=request.user)
    print(orders)
    return render(request, "home/orders.html", {"orders": orders})
