from django.urls import path
from user_payment import views

app_name = "user_payment"
urlpatterns = [
    # --- page that has pay now bottom that initiate payment session for test-- #
    path("product_page/<int:id>/", views.product_page, name="product_page"),
    # ------- successful page after payment success --------- #
    path("payment_successful/", views.payment_successful, name="product_page"),
    # ------- cancelled page after payment success --------- #
    path("payment_cancelled/", views.payment_cancelled, name="product_page"),
    # ------- stripe webhook --------- #
    path("stripe_webhook", views.stripe_webhook, name="stripe_webhook"),
]
