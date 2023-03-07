from django import forms

from fakecsvapp.models import Schema, SchemaColumn


class LoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)


class NewSchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['title', 'separator', 'string_character']


class NewColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaColumn
        fields = ['name', 'type', 'order']


class RowsAmountForm(forms.Form):
    rows = forms.IntegerField()
