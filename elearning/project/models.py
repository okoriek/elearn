from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.urls import reverse
import datetime

class MyUserManager(BaseUserManager):
    def create_user(self,email, first_name,last_name,password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,email,last_name,password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name = last_name,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    status = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    course = (
        ('Frontend(Html, Css, Javascript)', 'Frontend(Html, Css, Javascript)'),
        ('Backend(Python, Django)','Backend(Python, Django)'),
        ('App Development(React Native', 'App Development(React Native)'),
        ('Arduino(Software & Hardware)', 'Arduino(Software & Hardware)'),
    )
    first_name    = models.CharField(max_length=20)
    last_name     = models.CharField(max_length=20)
    email         = models.EmailField(max_length=100, unique=True)
    gender        = models.CharField(max_length=10, choices=status, blank=True, null=True)
    courses = models.CharField(max_length=200, choices=course, blank=True, null=True)
    phone_number  = models.CharField(max_length=100, blank=True, null=True)
    payment_done  = models.BooleanField(default=False)

    
    date_joined   = models.DateTimeField(auto_now_add=True) 
    last_login    = models.DateTimeField(auto_now_add=True)   
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
class Contact(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"{self.name} -------- {self.subject}"
    

class Tutorial_video(models.Model):
    status=(
        ('Frontend(Html, Css, Javascript)', 'Frontend(Html, Css, Javascript)'),
        ('Backend(Python, Django)','Backend(Python, Django)'),
        ('App Development(React Native', 'App Development(React Native)'),
        ('Arduino(Software & Hardware)', 'Arduino(Software & Hardware)'),
    )
    tags= models.CharField(max_length=50, choices=status, blank=True, null=True)
    title =  models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.FileField(upload_to='thumbnails/', blank=True, null=True)
    videos =  models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return f"{self.tags} {self.title} lesson{self.pk}"
    
    def get_absolute_url(self):
        return reverse('videosdetails', args=[self.pk])
    

class Ebook(models.Model):
    status=(
        ('Frontend(Html, Css, Javascript)', 'Frontend(Html, Css, Javascript)'),
        ('Backend(Python, Django)','Backend(Python, Django)'),
        ('App Development(React Native', 'App Development(React Native)'),
        ('Arduino(Software & Hardware)', 'Arduino(Software & Hardware)'),
    )
    tags = models.CharField(max_length=200, choices=status , blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description =  models.CharField(max_length=500, blank=True, null=True)
    img =  models.ImageField(upload_to='Images/', blank=True, null=True)
    ebook = models.FileField(upload_to='Ebooks/', blank=True, null=True)

    def __str__(self):
        return f"Title: {self.title} ---------- Description: {self.description}"

class Duration(models.Model):
    lesson = models.ForeignKey(Tutorial_video, on_delete=models.CASCADE, blank=True, null=True)
    deadline = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.deadline < timezone.now() :
            self.expired = True
        else:
            self.expired = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Topic: {self.lesson} ----------- Deadline: {self.deadline}"
    
    
class Assignment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Tutorial_video, on_delete=models.CASCADE, blank=True, null=True)
    result_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    feedback = models.TextField(max_length=500, blank=True, null=True)
    marked = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    
    def __str__(self):
        return f"User: {self.user.email} ----------- Topic: {self.lesson}"
    
class Total(models.Model):
    user =  models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    total =  models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}===> {self.total}"

    


    


    


