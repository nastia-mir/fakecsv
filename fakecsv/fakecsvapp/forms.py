from django.forms import PasswordInput, Form, CharField


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)
