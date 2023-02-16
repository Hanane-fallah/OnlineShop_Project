from django.urls import path
from .views import *


urlpatterns = [
    # path('', AdminIndex.as_view(), name='admin_index'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('verify/', UserVerify.as_view(), name='verify'),
    path('reset/', UserPasswordReset.as_view(), name='reset_password'),
    path('reset-done/', UserPasswordResetDone.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('confirm-complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('profile/<int:pk>/', UserDetailView.as_view(), name='user_profile'),

]