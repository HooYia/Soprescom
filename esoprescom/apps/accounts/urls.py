from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_user, name='logout_user'),
   
    #path('profile/<int:id>/', views.update_profile, name='profile'),
    path('profile/', views.update_profile, name='profile'),
    
    #users
    path('users/', views.users, name='users'),
    path('users/update/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('users/delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    
    
    

]
