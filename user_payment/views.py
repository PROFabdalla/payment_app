import time

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from order.models import Order
from user_payment.models import UserPayment
from sending_mail.tasks import payment_succeed_mail


@login_required(login_url="/auth/login/")
def product_page(request, id):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    order = Order.objects.filter(pk=id).first()
    price = round(order.total_price(), 2)
    print(order, "------------------")
    # ------------ when customer click pay_now ------ #
    # ---------- create stripe checkout_session ---------- #
    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "USD",
                        "product_data": {
                            "name": order.order_no,
                        },
                        "unit_amount_decimal": price,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            customer_creation="always",
            success_url="http://127.0.0.1:8000/user_payment/payment_successful/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/user_payment/payment_cancelled/",
        )
        return redirect(checkout_session.url, code=303)
    return render(request, "user_payment/product_page.html")


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    print(customer, "------------------customer-----------------")
    user_id = request.user.id
    user_payment = UserPayment.objects.get(app_user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()

    return render(request, "user_payment/successful_page.html", {"customer": customer})


def payment_cancelled(request):
    return render(request, "user_payment/cancel_page.html")


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        print("error1", e)
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("error2", e)
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        payment_succeed_mail.delay()
        session = event["data"]["object"]
        session_id = session.get("id", None)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)
