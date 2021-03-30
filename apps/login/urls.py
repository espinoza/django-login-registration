from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_and_registration_forms),
    path('login', views.login),
    path('registration', views.registration)
]
