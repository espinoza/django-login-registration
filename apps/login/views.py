from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm, RegisterForm
import bcrypt


def login_and_registration_forms(request):

    login_form = LoginForm()
    register_form = RegisterForm()

    context = {
        'login_form': login_form,
        'register_form': register_form
    }

    return render(request, "index.html",
                  {"login_form": login_form, "register_form": register_form})


def login(request):

    login_form = LoginForm(request.POST)
    register_form = RegisterForm()

    if login_form.is_valid():
        logged_user = User.objects.get(email=request.POST["email"])
        request.session['user_id'] = logged_user.id
        return redirect('/')

    login_form = LoginForm(request.POST)

    return render(request, "index.html",
                  {"login_form": login_form, "register_form": register_form})


def registration(request):

    print(request.POST)
    login_form = LoginForm()
    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        user = register_form.save(commit=False)
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
        user.password_hash = pw_hash
        user.save()
        register_form = RegisterForm()

    return render(request, "index.html",
                  {"login_form": login_form, "register_form": register_form})
