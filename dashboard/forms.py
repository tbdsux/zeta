from django import forms
from django.forms import widgets
from django.db.models import fields
from .models import Collections


class AddCollectionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=10,
        required=True,
        widget=widgets.TextInput(
            attrs={"placeholder": "What would you call your collection?"}
        ),
    )
    description = forms.CharField(
        max_length=30,
        required=True,
        widget=widgets.TextInput(
            attrs={"placeholder": "Enter some short description..."}
        ),
    )

    class Meta:
        model = Collections
        fields = ["name", "description"]
