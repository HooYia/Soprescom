from django.urls import path
from rest_registration.api.views import (
    change_password,
    login,
    logout,
    register,
    register_email,
    reset_password,
    send_reset_password_link,
    verify_email,
    verify_registration,
)

# from accounts.api.api import register_hooyia_view, verify_code

app_name = 'rest_registration'

urlpatterns = [

    path('register/', register, name='register'),
    
    
    path('login/', login, name='login'),


    path(
        'send-reset-password-link/', send_reset_password_link,
        name='send-reset-password-link',
    ),
    path('reset-password/', reset_password, name='reset-password'),

    path('logout/', logout, name='logout'),

    path('change-password/', change_password, name='change-password'),

    path('register-email/', register_email, name='register-email'),

    path('verify-email/', verify_email, name='verify-email'),

    path('verify-user/', verify_registration, name='verify_user'),
]