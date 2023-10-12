from .models import products,Products_Payments_Status,PaymentStatus
from demo_razpy.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
from datetime import datetime
from .models import Products_Payments_Status

def home(request):
    product = products.objects.all()
    context = {
        'p': product,
    }
    return render(request, "index.html", context)

def order_payment(request):
    if request.method == "POST":
        imageSrc = request.POST.get('imageSrc')
        title = request.POST.get('title')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        print(amount, type(amount))
        Amount = int(amount)  # Converting to an integer

        razorpay_order = client.order.create(
            {"amount": int(Amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        order = Products_Payments_Status.objects.create(
            p_name=title, price=int(Amount), p_img=imageSrc, desc=description, m_date=datetime.now(), provider_order_id=razorpay_order["id"]
        )

        order.save()

        return render(
            request,
            "payments/payment.html",
            {
                "callback_url": "http://127.0.0.1:5555/success/",  # Use the URL pattern name "callback"
                "razorpay_key": RAZORPAY_KEY_ID,
                "order": order,
                "amount": Amount,
            },
        )
    return redirect("/")

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    try:
        if "razorpay_signature" in request.POST:
            payment_id = request.POST.get("razorpay_payment_id", "")
            provider_order_id = request.POST.get("razorpay_order_id", "")
            signature_id = request.POST.get("razorpay_signature", "")
            order = Products_Payments_Status.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.signature_id = signature_id
            order.save()

            if verify_signature(request.POST):
                order.status = PaymentStatus.SUCCESS
            else:
                order.status = PaymentStatus.FAILURE
            order.save()

            return render(request, "payments/callback.html", context={"status": order.status})
        else:
            payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
            order = Products_Payments_Status.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "payments/callback.html", context={"status": order.status})
    except Exception as e:
        # Handle the exception as needed, such as rendering an error page or logging the error.
        print(f"An error occurred: {str(e)}")
        return redirect('/')
