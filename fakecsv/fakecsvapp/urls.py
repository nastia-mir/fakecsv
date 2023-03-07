from django.urls import path
from django.contrib.auth.decorators import login_required

from fakecsvapp import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('', login_required(views.HomeView.as_view()), name='home'),
    path('new/', login_required(views.NewSchemaView.as_view()), name='new schema'),
    path('new/<pk>/delete_column/', login_required(views.DeleteColumnView.as_view()), name='delete column'),
    path('<pk>/delete/', login_required(views.DeleteSchemaView.as_view()), name='delete schema'),
    path('<pk>/edit/', login_required(views.EditSchemaView.as_view()), name='edit schema'),

    path('<pk>/datasets', login_required(views.ShowSchemaView.as_view()), name='show schema'),

]
