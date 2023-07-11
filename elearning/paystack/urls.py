from django.urls import path
from . import views

app_name='paystack'

urlpatterns = [
    path('payment/<str:param>/', views.InitializePayment, name='payment'),
    path('confirmvoucher/', views.VoucherConfirm, name='confirmvoucher'),
    path('verify/<str:reference>/', views.verify_payment, name='verifypayment')
      
]
