from django.urls import path,include
from . import views

app_name='project'

urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.Register, name='register'),
    path('verification/<uidb64>/<token>/', views.EmailVerification, name='verification'),
    
]
