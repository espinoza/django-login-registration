from django import forms
from .models import User
import re
import bcrypt
from datetime import date

class RegisterForm(forms.ModelForm):

    password = forms.CharField(label="Create password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Write at least 8 characters",
                "type": "password",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'email',
        ]
        widgets = {
            'birthday' : forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'email': 'Your email',
        }

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        errors = password_errors(password)
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not is_valid_email(email):
            raise forms.ValidationError("Not valid email")
        user_with_email = User.objects.filter(email=email)
        if user_with_email:
            raise forms.ValidationError("Email is used by another user")
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if birthday > date.today():
            raise forms.ValidationError("Date must be past")
        if get_age(birthday) < 13:
            raise forms.ValidationError("You must be over 13 years old")
        return birthday


class LoginForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
            }
        )
    )

    class Meta:
        model = User
        fields = ['email']

    def clean(self):

        cleaned_data = super(LoginForm, self).clean()
        password = cleaned_data.get("password")
        email = cleaned_data.get("email")
        print(email, password)

        if not is_valid_email(email):
            raise forms.ValidationError("Not valid email")

        user = User.objects.filter(email=email)
        if not user:
            raise forms.ValidationError("There is no user with this email")

        logged_user = user[0]
        if not bcrypt.checkpw(password.encode(), logged_user.password_hash.encode()):
            raise forms.ValidationError("Wrong password")

        return cleaned_data


def get_age(birthDate):
    today = date.today()
    date_is_before_birthday = (today.month, today.day) \
                               < (birthDate.month, birthDate.day)
    age = today.year - birthDate.year - date_is_before_birthday
    return age


def contains_digit(string):
    RE_digit = re.compile('\d')
    return RE_digit.search(string)


def contains_uppercase(string):
    RE_upper = re.compile('[A-Z]')
    return RE_upper.search(string)


def is_valid_email(email):
    RE_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    return RE_EMAIL.match(email)


def password_errors(password):

    errors = []

    if len(password) < 8:
        errors.append("Password needs at least 8 characters")

    if not contains_digit(password):
        errors.append("Password needs at least one digit")

    if not contains_uppercase(password):
        errors.append("Password needs at least one uppercase letter")

    return errors

