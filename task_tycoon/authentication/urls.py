from django.urls import path
from .views import CreateUser, LoginUser, index

urlpatterns = [
    path('registration/', CreateUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('', index, name='home')
]
