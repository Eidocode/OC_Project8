from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
