from django import forms
from django.forms import widgets


class BrowseForm(forms.Form):
    TYPE_CLASS = (
        ("movie", "Movies"),
        ("series", "Series"),
        ("anime", "Anime"),
        ("book", "Books"),
        ("manga", "Manga"),
        ("asian drama", "Asian Drama"),
    )

    query = forms.CharField(
        max_length=50,
        required=True,
        widget=widgets.TextInput(attrs={"placeholder": "Enter something to search..."}),
    )
    type = forms.ChoiceField(widget=forms.Select, required=False, choices=TYPE_CLASS)
