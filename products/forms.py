from django import forms

import re


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-light', 'placeholder': 'Rechercher un produit...'}),
        required=True
    )

    print('*******')
    print("create form")
    print('*******')


    def clean(self):
        super(SearchForm, self).clean()

        search = self.cleaned_data.get('search')
        print('*******')
        print(search)
        print('*******')



        if len(search) < 2:
            self._errors['search'] = self.error_class([
                'Minimum 2 characters required'
            ])
        
        if bool(re.search(r"([^\w ^'])", search)):
            self._errors['search'] = self.error_class([
                'Special characters is not allowed'
            ])
        
        if bool(re.search(r"\d", search)):
            self._errors['search'] = self.error_class([
                'numeric characters is not allowed'
            ])

        return self.cleaned_data
