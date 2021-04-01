from django import forms
from .models import User
import bcrypt
from .utils import contains_digit, contains_uppercase, is_valid_email, get_age, is_past

class RegisterForm(forms.ModelForm):

    password = forms.CharField(label="Create password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Write at least 8 characters",
                "type": "password",
                "id": "id_password_registration",
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
            'birthday' : forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'id': 'id_email_registration'})
        }
        labels = {
            'email': 'Your email',
        }

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({"confirm_password": "Passwords don't match"})
        errors = password_errors(password)
        if errors:
            raise forms.ValidationError({"password": errors})
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        errors = validate_email(email)
        if errors:
            raise forms.ValidationError(errors)
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data.get("birthday")
        if not is_past(birthday):
            raise forms.ValidationError("Date must be past")
        if get_age(birthday) < 13:
            raise forms.ValidationError("You must be over 13 years old")
        return birthday

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) < 2:
            raise forms.ValidationError("First name needs 2 characters or more")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) < 2:
            raise forms.ValidationError("Last name needs 2 characters or more")
        return last_name


def validate_email(email):
    errors = []
    if not is_valid_email(email):
        errors.append("Not valid email")
    user_with_email = User.objects.filter(email=email)
    if user_with_email:
        errors.append("Email is used by another user")
    return errors


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

        if not is_valid_email(email):
            raise forms.ValidationError("Not valid email")

        user = User.objects.filter(email=email)
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(password.encode(), logged_user.password_hash.encode()):
                raise forms.ValidationError("Wrong password")
        else:
            raise forms.ValidationError("There is no user with this email")

        return cleaned_data


def password_errors(password):

    errors = []

    if len(password) < 8:
        errors.append("Password needs at least 8 characters")

    if not contains_digit(password):
        errors.append("Password needs at least one digit")

    if not contains_uppercase(password):
        errors.append("Password needs at least one uppercase letter")

    return errors

