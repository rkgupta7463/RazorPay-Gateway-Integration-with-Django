from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.
class products(models.Model):
    p_name=models.CharField(max_length=50)
    price=models.BigIntegerField()
    desc=models.TextField()
    p_img=models.ImageField()
    m_date=models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"{self.p_name} + {self.price}"
    

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"

NewPaymentStatus=PaymentStatus()

class Products_Payments_Status(models.Model):
    p_name=models.CharField(max_length=50)
    price=models.BigIntegerField()
    desc=models.TextField()
    p_img=models.ImageField()
    m_date=models.DateTimeField(auto_created=True)

    status = models.CharField(
        _("Payment Status"),
        default=NewPaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.p_name}-{self.status}-{self.price}"

