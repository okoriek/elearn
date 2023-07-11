from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('project.urls', namespace='project')),
    path('', include('paystack.urls', namespace='paystack'))
]
