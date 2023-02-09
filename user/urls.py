from django.urls import path
from .views import *


urlpatterns = [
    # path('', AdminIndex.as_view(), name='admin_index'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('verify/', UserVerify.as_view(), name='verify'),

]