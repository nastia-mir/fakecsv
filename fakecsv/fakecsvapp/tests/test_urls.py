from django.test import SimpleTestCase
from django.urls import reverse, resolve

from fakecsvapp import views


class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__, views.LoginView.as_view().__name__)

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.__name__, views.LogoutView.as_view().__name__)

    def test_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.__name__, views.HomeView.as_view().__name__)

    def test_new_schema(self):
        url = reverse('new schema')
        self.assertEqual(resolve(url).func.__name__, views.NewSchemaView.as_view().__name__)

    def test_delete_column(self):
        url = reverse('delete column', args={1})
        self.assertEqual(resolve(url).func.__name__, views.DeleteColumnView.as_view().__name__)

    def test_edit_schema(self):
        url = reverse('edit schema', args={1})
        self.assertEqual(resolve(url).func.__name__, views.EditSchemaView.as_view().__name__)

    def test_show_schema(self):
        url = reverse('show schema', args={1})
        self.assertEqual(resolve(url).func.__name__, views.ShowSchemaView.as_view().__name__)