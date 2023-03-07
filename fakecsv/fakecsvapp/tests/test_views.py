from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from fakecsvapp.models import Schema, SchemaColumn, DataSets


class TestViewsLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.new_schema_url = reverse('new schema')

        self.add_column_data_valid = {'name': 'name',
                                      'type': 'full_name',
                                      'order': 0}

        self.add_column_data_invalid_order = {'name': 'name',
                                              'type': 'full_name',
                                              'order': 'order'}

        self.new_schema_data = {'title': 'title',
                                'separator': ',',
                                'string_character': '"'}

        self.login_data = {'username': 'username',
                           'password': 'password'}

        self.valid_rows = {'rows': 10}
        self.invalid_rows = {'rows': 'rows'}

        self.client.post(self.login_url, self.login_data)

        self.user = User.objects.get(username='username')
        self.schema = Schema.objects.create(user=self.user)
        self.column = SchemaColumn.objects.create(schema=self.schema, name='name', type='full_name')

        self.delete_column_url = reverse('delete column', args={self.schema.id})
        self.delete_schema_url = reverse('delete schema', args={self.schema.id})
        self.edit_schema_url = reverse('edit schema', args={self.schema.id})
        self.show_schema_url = reverse('show schema', args={self.schema.id})
        return super().setUp()

    def test_HomeView_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_NewSchemaView_GET(self):
        response = self.client.get(self.new_schema_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_schema.html')

    def test_NewSchemaView_POST_new_column_valid(self):
        response = self.client.post(self.new_schema_url, self.add_column_data_valid)
        self.assertEqual(response.status_code, 302)

    def test_NewSchemaView_POST_new_column_invalid_order(self):
        response = self.client.post(self.new_schema_url, self.add_column_data_invalid_order)
        self.assertEqual(response.status_code, 302)

    def test_NewSchemaView_POST_new_column_no_data(self):
        response = self.client.post(self.new_schema_url, {})
        self.assertEqual(response.status_code, 302)

    def test_NewSchemaView_POST_save_schema_valid(self):
        response = self.client.post(self.new_schema_url, self.new_schema_data)
        self.assertEqual(response.status_code, 302)

    def test_NewSchemaView_POST_save_schema_no_data(self):
        response = self.client.post(self.new_schema_url, {})
        self.assertEqual(response.status_code, 302)

    def test_DeleteColumnView_GET_valid(self):
        self.client.get(self.new_schema_url)
        self.client.post(self.new_schema_url, self.add_column_data_valid)
        response = self.client.get(self.delete_column_url)
        self.assertEqual(response.status_code, 302)

    def test_DeleteColumnView_GET_column_dont_exists(self):
        response = self.client.get(self.delete_column_url)
        self.assertEqual(response.status_code, 302)

    def test_DeleteSchemaView_GET_valid(self):
        response = self.client.get(self.delete_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_DeleteSchemaView_GET_no_schema(self):
        self.client.get(self.delete_schema_url)
        response = self.client.get(self.delete_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_EditSchemaView_GET_valid(self):
        response = self.client.get(self.edit_schema_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_schema.html')

    def test_EditSchemaView_GET_schema_not_exists(self):
        self.client.get(self.delete_schema_url)
        response = self.client.get(self.edit_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_EditSchemaView_POST_add_column_valid(self):
        response = self.client.post(self.edit_schema_url, self.add_column_data_valid)
        self.assertEqual(response.status_code, 302)

    def test_EditSchemaView_POST_new_column_no_data(self):
        response = self.client.post(self.edit_schema_url, {})
        self.assertEqual(response.status_code, 302)

    def test_EditSchemaView_POST_save_schema_valid(self):
        response = self.client.post(self.edit_schema_url, self.new_schema_data)
        self.assertEqual(response.status_code, 302)

    def test_EditSchemaView_POST_save_schema_no_data(self):
        response = self.client.post(self.edit_schema_url, {})
        self.assertEqual(response.status_code, 302)

    def test_ShowSchemaView_GET_valid(self):
        response = self.client.get(self.show_schema_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_schema.html')

    def test_ShowSchemaView_GET_no_schema(self):
        self.client.get(self.delete_schema_url)
        response = self.client.get(self.show_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_ShowSchemaView_POST_valid(self):
        response = self.client.post(self.show_schema_url, self.valid_rows)
        self.assertEqual(response.status_code, 302)

    def test_ShowSchemaView_POST_invalid(self):
        response = self.client.post(self.show_schema_url, self.invalid_rows)
        self.assertEqual(response.status_code, 302)


class TestViewsNotLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.new_schema_url = reverse('new schema')
        self.delete_column_url = reverse('delete column', args={1})
        self.delete_schema_url = reverse('delete schema', args={1})
        self.edit_schema_url = reverse('edit schema', args={1})
        self.show_schema_url = reverse('show schema', args={1})
        return super().setUp()

    def test_HomeView_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)

    def test_NewSchemaView_GET(self):
        response = self.client.get(self.new_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_DeleteColumnView_GET(self):
        response = self.client.get(self.delete_column_url)
        self.assertEqual(response.status_code, 302)

    def test_DeleteSchemaView_GET(self):
        response = self.client.get(self.delete_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_EditSchemaView_GET(self):
        response = self.client.get(self.edit_schema_url)
        self.assertEqual(response.status_code, 302)

    def test_ShowSchemaView_GET(self):
        response = self.client.get(self.show_schema_url)
        self.assertEqual(response.status_code, 302)


class TestAuthView(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.login_data = {'username': 'username',
                           'password': 'password'}
        return super().setUp()

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_POST_correct_data(self):
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 302)

    def test_logout_GET_logged_in(self):
        self.client.get(self.login_url)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_logout_GET_not_logged_in(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
