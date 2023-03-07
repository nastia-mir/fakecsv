import re
import pathlib

from dateutil.parser import parse

from django.contrib.auth.models import User
from django.test import TestCase

from fakecsvapp import services
from fakecsvapp.models import Schema, SchemaColumn, DataSets


class TestColumns(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username', password='password')
        self.schema = Schema.objects.create(user=self.user)
        self.column = SchemaColumn.objects.create(type='full_name', name='name', schema=self.schema)

        return super().setUp()

    def test_normalise_column_orders_correct_order(self):
        order = 1
        normalized_order = services.Columns.normalise_column_orders(self.schema, order)
        self.assertEqual(normalized_order, 1)

    def test_normalise_column_orders_bigger_order(self):
        order = 3
        normalized_order = services.Columns.normalise_column_orders(self.schema, order)
        self.assertEqual(normalized_order, 1)

    def test_normalise_column_orders_existing_order(self):
        order = 0
        normalized_order = services.Columns.normalise_column_orders(self.schema, order)
        self.assertEqual(normalized_order, 0)


class TestFile(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='username', password='password')
        self.schema = Schema.objects.create(user=self.user)
        self.column = SchemaColumn.objects.create(type='full_name', name='name', schema=self.schema)
        self.dataset = DataSets.objects.create(schema=self.schema, rows_amount=10)
        return super().setUp()

    def test_email_generator(self):
        email = services.File.get_email()
        self.assertTrue('@gmail.com' in email)

    def test_domain_generator(self):
        domain = services.File.get_domain()
        self.assertTrue('www.' in domain)

    def test_phone_number_generator(self):
        phone_number = services.File.get_phone_number()
        pattern = re.compile("^(\+\d{16})")
        pattern.match(phone_number)
        self.assertTrue(pattern.match(phone_number))

    def test_date_generator(self):
        date = services.File.get_date()
        self.assertTrue(parse(date))

    def test_file_created(self):
        services.File.generate_csv(self.dataset)
        file = pathlib.Path("fakecsv/media/{}{}.csv".format(self.schema.title, self.dataset.id))
        self.assertTrue(file.exists())



