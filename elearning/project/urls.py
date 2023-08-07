from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls.base import reverse_lazy



urlpatterns = [
    path('', views.Home, name='home'),
    path('contact/', views.Contact, name='contact'),
    path('register/', views.Register, name='register'),
    path('verification/<uidb64>/<token>/', views.EmailVerification, name='verification'),
    path('profile/', views.Dashboard, name='dashboard'),
    path('tutorial_vidoes/', views.GetVideos, name='videos' ),
    path('playing/videos/<int:pk>/', views.GetVideosDetail, name='videosdetails'),
    path('online-ebook/', views.GetEbook, name='ebook'),
    path('rankings/', views.LeaderBoard, name='ranking'),
    path('tasks_submiting/', views.Task, name='assignment'),
    path('edit_response/', views.EditTask, name='edit'),

    #generic views

    path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_reset/', PasswordResetView.as_view(template_name='project/password/passwordreset.html'), name='reset_password'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='project/password/passwordresetdone.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='project/password/passwordresetconfirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name='project/password/passwordresetcomplete.html'), name='password_reset_complete'),
    
    
]
