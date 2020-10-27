from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import widgets

# add email to the default usercreation form of django
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email address"}),
        label="Email Address",
    )
    agree = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "agree")
        widgets = {
            "username": widgets.TextInput(attrs={"placeholder": "Enter your username"}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget = widgets.PasswordInput(
            attrs={"placeholder": "Enter your password"}
        )
        self.fields["password2"].widget = widgets.PasswordInput(
            attrs={"placeholder": "Confirm your password"}
        )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


# add placeholder for the default login forms
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(
            attrs={"placeholder": "Your username"}
        )
        self.fields["password"].widget = widgets.PasswordInput(
            attrs={"placeholder": "Your password"}
        )
