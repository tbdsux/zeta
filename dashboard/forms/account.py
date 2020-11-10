from django import forms

# Custom User Info Update Form
class UpdateUserInfo(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=12,
        widget=forms.TextInput(attrs={"placeholder": "Enter a new username"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter a new email"}),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter a new password"}),
    )