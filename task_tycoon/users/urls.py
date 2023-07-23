from django.urls import path, include
from .views import index

urlpatterns = [
    path('success/', index, name='success')
]
