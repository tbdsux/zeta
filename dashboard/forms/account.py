from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Custom User Info Update Form (Username)
class UpdateUserInfoUsername(forms.ModelForm):
    action = forms.CharField(widget=forms.HiddenInput, max_length=20)
    username = forms.CharField(
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "Enter a new username"}),
    )

    class Meta:
        model = User
        fields = ["action", "username"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateUserInfoUsername, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]

        # check if username is similar to current username
        if username == self.user.username:
            raise ValidationError("You need to have a different username to update!")

        # check if the username exists
        user = User.objects.filter(username=username)
        if user:
            raise ValidationError("That username already exist!")

        return username

    def save(self, commit=True):
        username = self.cleaned_data["username"]
        self.user.username = username

        if commit:
            self.user.save()

        return self.user


# Custom User Info Update Form (Email)
class UpdateUserInfoEmail(forms.ModelForm):
    action = forms.CharField(widget=forms.HiddenInput, max_length=20)
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter a new email"}),
    )

    class Meta:
        model = User
        fields = ["action", "email"]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UpdateUserInfoEmail, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]

        # check if email is similar to current email
        if email == self.user.email:
            raise ValidationError("You need to have a different email to update!")

        # check if the email exists
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("That email already exist!")

        return email

    def save(self, commit=True):
        email = self.cleaned_data["email"]
        self.user.email = email

        if commit:
            self.user.save()

        return self.user


# Update Password Form
class UpdatePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your old password..."}),
    )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your new password"}),
    )
    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your new password"}),
    )
