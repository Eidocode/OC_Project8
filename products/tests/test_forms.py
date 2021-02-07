from django.test import TestCase

from products.forms import SearchForm


class SearchFormTest(TestCase):

    def test_search_form_field_label(self):
        form = SearchForm()
        self.assertTrue(form.fields['search'].label is None)

    def test_search_form_max_length(self):
        form = SearchForm()
        max_length = form.fields['search'].max_length
        self.assertEquals(max_length, 30)

    def test_search_form_is_required(self):
        form = SearchForm()
        required = form.fields['search'].required
        self.assertTrue(required)

    def test_search_form_widget_attrs_class(self):
        form = SearchForm()
        attr = form.fields['search'].widget.attrs['class']
        self.assertEquals(attr, 'form-control form-control-lg bg-light')

    def test_search_form_widget_attrs_placeholder(self):
        form = SearchForm()
        attr = form.fields['search'].widget.attrs['placeholder']
        self.assertEquals(attr, 'Rechercher un produit...')
