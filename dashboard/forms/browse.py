from django import forms
from django.forms import widgets


class BrowseForm(forms.Form):
    query = forms.CharField(
        max_length=50,
        required=True,
        widget=widgets.TextInput(attrs={"placeholder": "Enter something to search..."}),
    )
