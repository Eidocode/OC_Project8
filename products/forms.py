from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-light', 'placeholder': 'Rechercher un produit...'}),
        required=True
    )

    def clean(self):
        super(SearchForm, self).clean()

        search = self.cleaned_data.get('search')

        if len(search) < 2:
            self._errors['search'] = self.error_class([
                'Minimum 2 characters required'
            ])
        
        

        return self.cleaned_data
