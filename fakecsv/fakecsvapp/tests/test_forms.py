from django.test import TestCase

from fakecsvapp import forms


class TestForms(TestCase):
    def test_LoginForm_valid_data(self):
        form = forms.LoginForm(data={
            'username': 'username',
            'password': 'password'
        })
        self.assertTrue(form.is_valid())

    def test_LoginForm_no_data_form_invalid(self):
        form = forms.LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_NewSchemaForm_valid_data(self):
        form = forms.NewSchemaForm(data={
            'title': 'title',
            'separator': ',',
            'string_character': '"'
        })
        self.assertTrue(form.is_valid())

    def test_NewSchemaForm_no_data(self):
        form = forms.NewSchemaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_NewSchemaForm_invalid_data(self):
        form = forms.NewSchemaForm(data={
            'title': 'title',
            'separator': ':',
            'string_character': ':'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_NewColumnForm_valid_data(self):
        form = forms.NewColumnForm(data={
            'name': 'name',
            'type': 'full_name',
            'order': 0
        })
        self.assertTrue(form.is_valid())

    def test_NewColumnForm_no_data(self):
        form = forms.NewColumnForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_NewColumnForm_invalid_data(self):
        form = forms.NewColumnForm(data={
            'name': 'name',
            'type': 'full_name',
            'order': 'somestring'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def testRowsAmountForm_valid_data(self):
        form = forms.RowsAmountForm(data={
            'rows': 25,
        })
        self.assertTrue(form.is_valid())

    def test_RowsAmountForm_no_data(self):
        form = forms.RowsAmountForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_RowsAmountForm_invalid_data(self):
        form = forms.RowsAmountForm(data={
            'rows': 'rows',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

