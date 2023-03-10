from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib import messages

from django.shortcuts import render, redirect, reverse
from django.views.generic import View, TemplateView
from django.views.generic.edit import ProcessFormView

from fakecsvapp.forms import LoginForm, NewSchemaForm, NewColumnForm, RowsAmountForm
from fakecsvapp.models import Schema, SchemaColumn, DataSets
from fakecsvapp.services import Columns, File


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password,)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                new_user = User.objects.create_user(username=username, password=password)
                login(request, new_user)
                return redirect('home')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        schemas = list(Schema.objects.filter(user=self.request.user).order_by('date_modified'))
        context['schemas'] = zip(schemas, range(1, len(schemas)+1))
        return context


class NewSchemaView(ProcessFormView):
    template_name = 'edit_schema.html'

    def get(self, request):
        context = {'schema_form': NewSchemaForm(),
                   'column_form': NewColumnForm(),
                   'url': reverse('new schema')
                   }
        draft = cache.get('draft')
        if not draft:
            draft, created = Schema.objects.get_or_create(user=request.user, is_draft=True)
            cache.set('draft', draft, 30)
        columns = list(SchemaColumn.objects.filter(schema=draft).order_by('order'))
        if len(columns) != 0:
            context['columns'] = columns
        else:
            context['columns'] = None
        return render(request, self.template_name, context)

    def post(self, request):
        schema = cache.get('draft')
        if not schema:
            schema = Schema.objects.get(user=request.user, is_draft=True)
            cache.set('draft', schema, 30)
        if 'create_schema' in request.POST:
            form = NewSchemaForm(request.POST)
            if form.is_valid():
                schema_form = form.save(commit=False)
                schema.title = schema_form.title
                schema.separator = schema_form.separator
                schema.string_character = schema_form.string_character
                schema.is_draft = False
                schema.save()
                cache.delete('draft')
                return redirect('home')
            else:
                messages.error(request, 'Something went wrong with schema.')
                return redirect('new schema')
        elif 'add_column' in request.POST:
            form = NewColumnForm(request.POST)
            if form.is_valid():
                column_form = form.save(commit=False)
                column_form.schema = schema
                column_form.order = Columns.normalise_column_orders(schema, column_form.order)
                column_form.save()
                return redirect('new schema')
            else:
                messages.error(request, 'Something went wrong with new column.')
                return redirect('new schema')
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('new schema')


class DeleteColumnView(View):
    def get(self, request, pk):
        try:
            column = SchemaColumn.objects.get(id=pk)
            column.delete()
            deleted_order = column.order
            next_columns = list(SchemaColumn.objects.filter(schema=column.schema, order__gte=deleted_order))
            for column in next_columns:
                column.order = column.order - 1
                column.save()

            if column.schema.is_draft:
                return redirect('new schema')
            else:
                return redirect(reverse('edit schema', args={column.schema.id}))
        except:
            return redirect('new schema')


class DeleteSchemaView(View):
    def get(self, request, pk):
        try:
            schema = Schema.objects.get(id=pk)
            schema.delete()
            return redirect('home')
        except:
            return redirect('home')


class EditSchemaView(View):
    template_name = 'edit_schema.html'

    def get(self, request, pk):
        try:
            schema = Schema.objects.get(id=pk)
        except:
            return redirect('home')
        cache.set('schema', schema, 30)

        context = {'schema_form': NewSchemaForm(instance=schema),
                   'column_form': NewColumnForm()
                   }
        columns = list(SchemaColumn.objects.filter(schema=schema).order_by('order'))
        if len(columns) != 0:
            context['columns'] = columns
        else:
            context['columns'] = None
        return render(request, self.template_name, context)

    def post(self, request, pk):
        schema = cache.get('schema')
        if not schema:
            schema = Schema.objects.get(id=pk)
            cache.set('schema', schema, 30)
        if 'create_schema' in request.POST:
            form = NewSchemaForm(request.POST)
            if form.is_valid():
                schema_form = form.save(commit=False)
                schema.title = schema_form.title
                schema.separator = schema_form.separator
                schema.string_character = schema_form.string_character
                schema.save()
                cache.delete('schema')
                return redirect('home')
            else:
                messages.error(request, 'Something went wrong with schema.')
                return redirect('edit schema')
        elif 'add_column' in request.POST:
            form = NewColumnForm(request.POST)
            if form.is_valid():
                column_form = form.save(commit=False)
                column_form.schema = schema
                column_form.order = Columns.normalise_column_orders(schema, column_form.order)
                column_form.save()
                return redirect(reverse('edit schema', args={schema.id}))
            else:
                messages.error(request, 'Something went wrong with new column.')
                return redirect(reverse('edit schema', args={schema.id}))
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('edit schema')


class ShowSchemaView(View):
    def get(self, request, pk):
        context = {}
        schema = cache.get('schema')
        if not schema:
            try:
                schema = Schema.objects.get(id=pk)
            except:
                return redirect('home')
            cache.set('schema', schema, 900)
        context['schema'] = schema
        schema_columns = list(SchemaColumn.objects.filter(schema=schema))
        context['columns'] = zip(schema_columns, range(1, len(schema_columns) + 1))
        context['form'] = RowsAmountForm()

        data_sets = list(DataSets.objects.filter(schema=schema))
        if len(data_sets) != 0:
            context['data_sets'] = zip(data_sets, range(1, len(data_sets) + 1))
        else:
            context['data_sets'] = None
        return render(request, 'show_schema.html', context)

    def post(self, request, pk):
        schema = cache.get('schema')
        if not schema:
            try:
                schema = Schema.objects.get(id=pk)
            except:
                return redirect('home')
            cache.set('schema', schema, 900)

        form = RowsAmountForm(request.POST)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            dataset = DataSets.objects.create(rows_amount=rows, schema=schema)
            File.generate_csv(dataset)
            file = f'{dataset.schema.title}{dataset.id}.csv'
            dataset.csv_file = file
            dataset.status = 'ready'
            dataset.save()
            return redirect(reverse('show schema', args={pk}))
        else:
            messages.error(request, 'Enter valid number.')
            return redirect(reverse('show schema', args={pk}))

