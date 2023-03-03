from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from fakecsvapp.forms import LoginForm


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

            user = authenticate(
                username=username,
                password=password,
            )
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
