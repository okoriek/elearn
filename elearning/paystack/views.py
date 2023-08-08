from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from  paystack.models import *
from project.models import Account
from django.conf import settings
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required(login_url='/login/')
def VoucherConfirm(request):
    voucher = request.POST['voucher']
    try:
        bonus = Voucher.objects.get(voucher = voucher)
        if bonus:
            return JsonResponse({'percent':bonus.percent, 'message':'Voucher Activated'})
    except:
        return JsonResponse('Invalid Voucher', safe=False)
        

@login_required(login_url='/login/')
def InitializePayment(request, param):
    uid =  force_str(urlsafe_base64_decode(param))
    user = Account.objects.get(pk=uid)
    payment =  Paystack.objects.create(email=user.email, amount = int(20000))
    payment.save()
    arg = {'user':user, 'payment':payment, 'PUBLIC_KEY':os.environ.get('PAYSTACK_PUBLIC_KEY')}
    print(os.environ.get('PAYSTACK_PUBLIC_KEY'))
    return render(request, 'payment.html', arg)


@login_required(login_url='/login/')
def verify_payment(request, reference):
    payment = get_object_or_404(Paystack, reference=reference)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Successful Deposit')
    else:
        messages.error(request, 'Incomplete Deposit Transaction')
    return redirect('/')
        
    
    