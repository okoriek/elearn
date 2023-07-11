from django.shortcuts import render,redirect
from . models import *
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegistrationForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .utils import TokenGenerator
from django.template.loader import render_to_string

def Home(request):
    return render(request, 'project/index.html')

def EmailVerification(request, uidb64, token):
    try:
        uid =  force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError,ValueError, OverflowError, Account.DoesNotExist):
        user = None
        return HttpResponse(request, 'Your account could not be verified ')
    if user is not None and TokenGenerator.check_token(user, token):
        user.is_active =  True
        user.save()
        messages.success(request, 'Your Email as been verified')
        return redirect('paystack:payment', param=uidb64)
    

def Register(request):

    if request.method == 'POST':
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.save()
            website = get_current_site(request).domain
            email_subject = 'Email Verification'
            email_body =  render_to_string('project/activation.html',{
                'user':user.first_name,
                'domain':website,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': TokenGenerator.make_token(user)
            })
            email = EmailMessage(subject=email_subject, body=email_body,
                from_email='Crimsonic Elearning <admin@stormxbet.com>', to=[user.email]
                )
            email.content_subtype='html'
            email.send()
            messages.success(request, 'A Verification Mail has been sent to your Email,Activate your account to Login')
            return redirect('/')
    else:
        forms = RegistrationForm()
    args = {'forms':forms}
    return render(request, 'project/register.html', args)

