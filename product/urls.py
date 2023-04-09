from django.urls import path

from product.views import ProductDefaultImage, ProductDetails, ProductView

urlpatterns = [
    path("", ProductView.as_view(), name="products"),
    path("<int:pk>/", ProductDetails.as_view(), name="product_details"),
    path("default/", ProductDefaultImage.as_view(), name="product_image"),
]
