from django.db import models
from django.utils import timezone
import secrets
from .paystack import PayStackPayment
from project.models import *





class Paystack(models.Model):
    amount = models.CharField(max_length=1000000)
    email =  models.EmailField(max_length=3000, blank=True, null=True)
    reference = models.CharField(max_length=200)
    generated = models.DateTimeField(default=timezone.now)
    verified =  models.BooleanField(default=False)

    class Meta:
        ordering = ('-generated',)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        while not self.reference:
            ref = secrets.token_urlsafe(50)
            same_ref = Paystack.objects.filter(reference = ref)
            if not same_ref:
                self.reference = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return int(self.amount)*100

    def verify_payment(self):
        paystack = PayStackPayment()
        status, result = paystack.verify_payment(self.reference, self.amount)
        if status:
            if result['amount']/100 == int(self.amount) or int(5000):
                self.amount = result['amount']/100
                self.verified = True
            self.save()
        if self.verified:
            user = Account.objects.get(email = self.email)
            user.payment_done=True
            user.save()
            return True
        return False
    

class Voucher(models.Model):
    voucher =  models.CharField(max_length=10)
    percent =  models.IntegerField(default=0)
    
    def __str__(self):
        return self.voucher



    
    
        