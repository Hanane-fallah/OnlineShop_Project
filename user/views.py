from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .decorators import unauthenticated_user
from django.utils.decorators import method_decorator
from .forms import CustomerCreationFrom


@method_decorator(unauthenticated_user, name='get')
class RegisterPage(View):
    def get(self, request):
        form = CustomerCreationFrom()
        context = {
            'form': form
        }
        return render(request, 'account/register.html', context=context)

    def post(self, request):
        form = CustomerCreationFrom(request.POST)

        if form.is_valid():
            user = form.save()
            if 'admin' in request.POST:
                admin_type = request.POST.get('admin')
                group = Group.objects.get(name=admin_type)
                user.groups.add(group)
                user.is_staff = True
                user.save()
                return redirect('admin:index')

            return redirect('account:login')
        else:
            context = {
                'form': form
            }
            return render(request, 'account/register.html', context=context)


@method_decorator(unauthenticated_user, name='get')
class LoginPage(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        # username = form.get(/)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj:
            messages.success(request, 'User Loged in successfully')
            login(request, user_obj)
        else:
            messages.info(request, 'username or pass incorrect')
        return redirect('account:login')


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')

