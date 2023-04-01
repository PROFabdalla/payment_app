from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.shortcuts import redirect
import time
from django.http import HttpResponse
from user_payment.models import UserPayment
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/auth/login/")
def product_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    # ------------ when customer click pay_now ------ #
    # ---------- create stripe checkout_session ---------- #
    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            line_items=[{"price": settings.PRODUCT_PRICE, "quantity": 1}],
            mode="payment",
            customer_creation="always",
            success_url=settings.REDIRECT_DOMAIN
            + "user_payment/payment_successful/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.REDIRECT_DOMAIN + "user_payment/payment_cancelled/",
        )
        return redirect(checkout_session.url, code=303)
    return render(request, "user_payment/product_page.html")


def payment_successful(request):
    return render(request, "user_payment/successful_page.html")


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
        print(e)
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id", None)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
        return HttpResponse(status=200)
