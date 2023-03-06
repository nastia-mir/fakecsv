from django.db import models
from django.contrib.auth.models import User


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


class DataSets(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='schema_csv')
    rows_amount = models.IntegerField(blank=False)
    csv_file = models.FileField(upload_to='media/', max_length=254, null=True, blank=True)
    status_options = (
        ('processing', 'Processing'),
        ('ready', 'Ready')
    )
    status = models.CharField(max_length=100, choices=status_options, default='processing')
    created = models.DateField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return 'Schema {}, file {}'.format(self.schema, self.csv_file)
