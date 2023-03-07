import random
import itertools
import string
import csv
import rstr
import datetime
import pathlib

from fakecsvapp.models import SchemaColumn


class Columns:
    @classmethod
    def normalise_column_orders(cls, schema, new_col_order):
        try:
            order_exists = SchemaColumn.objects.get(schema=schema, order=new_col_order)
            previous_columns = list(SchemaColumn.objects.filter(schema=schema, order__gte=new_col_order))
            for column in previous_columns:
                column.order = column.order + 1
                column.save()
        except:
            columns_num = SchemaColumn.objects.filter(schema=schema).count()
            if new_col_order > columns_num:
                new_col_order = columns_num

        return new_col_order


class File:
    @classmethod
    def get_full_name(cls):
        first_names = ['Jonathan', 'Martin', 'Timothy', 'Sasha', 'Elias', 'Georgie', 'Basira', 'Alice', 'Melanie',
                       'Jurgen', 'Julia', 'Gertrude', 'Gerard', 'Agnes', 'Annabelle', 'Jane', 'Jonah', 'Michael',
                       'Peter', 'Trevor']
        last_names = ['Sims', 'Blackwood', 'Stoker', 'James', 'Bouchard', 'Barker', 'Hussain', 'Tonner', 'King',
                      'Leitner', 'Montauk', 'Robinson', 'Keay', 'Montague', 'Cane', 'Prentiss', 'Magnus', 'Crew',
                      'Lukas', 'Herbert']

        full_name = (random.choice(first_names), random.choice(last_names))
        return '{} {}'.format(full_name[0], full_name[1])

    @classmethod
    def get_email(cls):
        email = ''.join((random.choice(string.ascii_lowercase) for x in range(10))) + '@gmail.com'
        return email

    @classmethod
    def get_domain(cls):
        domain = 'www.' + ''.join((random.choice(string.ascii_lowercase) for x in range(10))) + '.com'
        return domain

    @classmethod
    def get_phone_number(cls):
        phone_number = rstr.xeger(r'^(\+\d{16})')
        return phone_number

    @classmethod
    def get_date(cls):
        now = datetime.datetime.now()
        random_date = now + datetime.timedelta(days=random.randint(-24000, 24000))
        return str(random_date)[:10]

    @classmethod
    def generate_csv(cls, dataset):
        rows = dataset.rows_amount
        columns = list(SchemaColumn.objects.filter(schema=dataset.schema).order_by('order'))
        column_dict = {}
        for column in columns:
            column_dict[column.type] = column.name

        with open('fakecsv/media/{}{}.csv'.format(dataset.schema.title, dataset.id), 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=dataset.schema.separator, quotechar=dataset.schema.string_character)
            row_list = [list(column_dict.values())]
            while len(row_list) < rows + 1:
                row = []
                for col_type in column_dict.keys():
                    if col_type == 'full_name':
                        row.append(cls.get_full_name())
                    elif col_type == 'email':
                        row.append(cls.get_email())
                    elif col_type == 'domain':
                        row.append(cls.get_domain())
                    elif col_type == 'phone_number':
                        row.append(cls.get_phone_number())
                    elif col_type == 'date':
                        row.append(cls.get_date())
                row_list.append(row)
            writer.writerows(row_list)

