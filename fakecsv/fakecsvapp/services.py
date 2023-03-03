from fakecsvapp.models import Schema, SchemaColumn


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

