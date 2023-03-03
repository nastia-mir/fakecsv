from django.urls import path
from django.contrib.auth.decorators import login_required

from fakecsvapp import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', login_required(views.HomeView.as_view()), name='home'),


]
