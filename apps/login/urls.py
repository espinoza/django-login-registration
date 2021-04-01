from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_and_registration_forms),
    path('login', views.login),
    path('registration', views.registration),
    path('success', views.success),
    path('logout', views.logout, name='logout'),
    path('validate_email', views.validate_email_now),
]
