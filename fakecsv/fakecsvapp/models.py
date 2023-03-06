from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class FullNameColumn(models.Model):
    column_name = models.CharField(max_length=150, default='Full name')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    objects = models.Manager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class EmailColumn(models.Model):
    column_name = models.CharField(max_length=150, default='Email')
    email = models.EmailField(max_length=150)

    objects = models.Manager()

    def __str__(self):
        return self.email


class DomainNameColumn(models.Model):
    column_name = models.CharField(max_length=150, default='Domain name')
    domain_name = models.CharField(max_length=150)

    objects = models.Manager()

    def __str__(self):
        return 'www.{}.com'.format(self.domain_name)


class PhoneNumberColumn(models.Model):
    column_name = models.CharField(max_length=150, default='Phone number')
    phone_regex = RegexValidator(regex=r'^(\+\d{16}')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    objects = models.Manager()

    def __str__(self):
        return self.phone_number


class DateColumn(models.Model):
    column_name = models.CharField(max_length=150, default='Date')
    date = models.DateField(auto_now=False, auto_now_add=False)

    objects = models.Manager()

    def __str__(self):
        return self.date


class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=150, default='My new schema')
    date_modified = models.DateField(auto_now=True)
    separator_options = (
        (',', 'Comma (,)'),
        (';', 'Semicolon (;)')
    )
    separator = models.CharField(max_length=50, choices=separator_options, default=',')

    string_options = (
        ('"', 'Double-quote (")'),
        ("'", "Single-quote (')")
    )
    string_character = models.CharField(max_length=50, choices=string_options, default='"')

    is_draft = models.BooleanField(default=True)

    objects = models.Manager()

    def __str__(self):
        return "{}'s schema {}".format(self.user, self.title)


class SchemaColumn(models.Model):
    types = (
        ('full_name', 'Full name'),
        ('email', 'Email'),
        ('domain', 'Domain name'),
        ('phone_number', 'Phone number'),
        ('date', 'Date'),
    )
    type = models.CharField(max_length=150, choices=types, blank=False)
    name = models.CharField(max_length=150, blank=False)
    order = models.IntegerField(default=0)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='schema')

    objects = models.Manager()

    def __str__(self):
        return 'Type: {}, name: {}'.format(self.get_type_display(), self.name)
