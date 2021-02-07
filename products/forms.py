from django import forms

import re


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-light', 'placeholder': 'Rechercher un produit...'}),
        required=True
    )

    def clean(self):
        super(SearchForm, self).clean()
        search = self.cleaned_data.get('search')

        if len(search) < 2:
            self._errors['search'] = self.error_class([
                'Saisir, au minimum, deux caractères pour valider la recherche'
            ])

        if bool(re.search(r"([^\w ^'])", search)):
            self._errors['search'] = self.error_class([
                'Les caractères spéciaux ne sont pas autorisés'
            ])

        if bool(re.search(r"\d", search)):
            self._errors['search'] = self.error_class([
                'Les chiffres ne sont pas autorisés'
            ])

        return search
