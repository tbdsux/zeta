from django import forms
from django.forms import widgets
from dashboard.models.collections import Collections


class AddUpdateCollectionForm(forms.ModelForm):
    TYPE_CLASS = (
        ("movie", "Movies"),
        ("series", "Series"),
        ("anime", "Anime"),
        ("book", "Books"),
        ("manga", "Manga"),
        ("asian drama", "Asian Drama"),
    )

    name = forms.CharField(
        max_length=20,
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
    type = forms.ChoiceField(widget=forms.Select, required=True, choices=TYPE_CLASS)

    class Meta:
        model = Collections
        fields = ["name", "description", "type"]