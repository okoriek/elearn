from django.shortcuts import render,redirect
from . models import *
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from django import urls
from django.http import HttpResponse, JsonResponse
from .forms import RegistrationForm, AssignmentForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .utils import TokenGenerator
from django.template.loader import render_to_string

def Home(request):
    return render(request, 'project/index.html')

def Contact(request):
    return render(request, 'project/contact.html')

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
                from_email='Crimsonic Learning Centre <admin@crimsoniclearningcentre.com.ng>', to=[user.email]
                )
            email.content_subtype='html'
            email.send()
            messages.success(request, 'A Verification Mail has been sent to your Email,Activate your account to Login')
            return redirect('/login/')
    else:
        forms = RegistrationForm()
    args = {'forms':forms}
    return render(request, 'project/register.html', args)


def Dashboard(request):
    
    return render(request, 'project/profile.html')

def GetVideos(reqeust):
    user = reqeust.user
    videos =  Tutorial_video.objects.filter(tags=user.courses)
    args = {'videos':videos}
    return render(reqeust, 'project/videos.html', args)

def GetVideosDetail(request, pk):
    video =  Tutorial_video.objects.get(pk=pk)
    args = {'data':video}
    return render(request, 'project/playvideo.html', args)


def GetEbook(request):
    user = request.user
    ebook = Ebook.objects.filter(tags=user.courses)
    args = {'books':ebook}
    return render(request, 'project/ebooks.html',args)

def LeaderBoard(request):
    user = Total.objects.all()
    args = {'users':user}
    return render(request, 'project/ranking.html', args)

def Task(request):
    time = Duration.objects.last()
    lesson = Tutorial_video.objects.last()
    time.save()
    if request.method == 'POST':
        form =  AssignmentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.submitted = True
            data.save()
            return redirect(Task)
    else:
        form = AssignmentForm()
    try:
        submit = Assignment.objects.get(user=request.user, lesson = lesson, submitted = True)
        if submit: 
            args = {'forms':form, 'edit':submit}
            return render(request, 'project/assignment.html', args )
    except:
        if time.expired:
            args = None
            return render(request, 'project/assignment.html', args )
        kwarg = {'forms':form }
        return render(request, 'project/assignment.html', kwarg )
    
def EditTask(request):
    user = request.user
    lesson = Tutorial_video.objects.last()
    task = Assignment.objects.filter(user=user, submitted =True, lesson=lesson, marked=False).last()
    form = AssignmentForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Updated Task Successfully')
        return redirect(Task)
    else:
        form = AssignmentForm(instance=task)
    arg = {'forms': form}
    return render(request, 'project/editassignment.html', arg)

    
    