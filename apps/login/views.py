from django.shortcuts import render
from .models import User
from .forms import LoginForm, RegisterForm


def login(request):

    if request.method == "GET":
        login_form = LoginForm()
        register_form = RegisterForm()
    else:
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)

    context = {
        'login_form': login_form,
        'register_form': register_form
    }

    return render(request, "login.html", context)
