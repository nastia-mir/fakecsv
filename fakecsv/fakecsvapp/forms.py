from django import forms

from fakecsvapp.models import Schema, SchemaColumn


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class NewSchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['title', 'separator', 'string_character']


class NewColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaColumn
        fields = ['name', 'type', 'order']
