from django import forms

from fakecsvapp.models import Schema, SchemaColumn


class LoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)


class NewSchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['title', 'separator', 'string_character']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'separator': forms.Select(attrs={'class': 'form-control'}),
            'string_character': forms.Select(attrs={'class': 'form-control'})
        }


class NewColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaColumn
        fields = ['name', 'type', 'order']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.TextInput(attrs={'class': 'form-control'})
        }


class RowsAmountForm(forms.Form):
    rows = forms.IntegerField()
