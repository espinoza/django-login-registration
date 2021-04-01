from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm, RegisterForm
import bcrypt
from .forms import validate_email
from django.http import JsonResponse


def login_and_registration_forms(request):

    if "user_id" in request.session:
        return redirect('/success')

    login_form = LoginForm()
    register_form = RegisterForm()

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }

    return render(request, "index.html", context)


def login(request):

    login_form = LoginForm(request.POST)
    register_form = RegisterForm()

    if login_form.is_valid():
        logged_user = User.objects.get(email=request.POST["email"])
        request.session['user_id'] = logged_user.id
        request.session['recently_registered'] = False
        return redirect('/success')

    login_form = LoginForm(request.POST)

    context = {
        'login_form': login_form,
        'register_form': register_form
    }

    return render(request, "index.html", context)


def registration(request):

    print(request.POST)
    login_form = LoginForm()
    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        registered_user = register_form.save(commit=False)
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        registered_user.password_hash = pw_hash
        registered_user.save()
        request.session['user_id'] = registered_user.id
        request.session['recently_registered'] = True
        return redirect('/success')

    context = {
        'login_form': login_form,
        'register_form': register_form
    }

    return render(request, "index.html", context)


def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session["user_id"])
    status = "logged in"
    if "recently_registered" in request.session:
        if request.session["recently_registered"]:
            status = "registered"

    return render(request, "success.html", {"user": user, "status": status})


def logout(request):
    del request.session["user_id"]
    return redirect('/')


def validate_email_now(request):
    print("validate email!!!!!!!!!!!")
    errors = validate_email(request.POST["email"])
    return JsonResponse({"errors": errors})

