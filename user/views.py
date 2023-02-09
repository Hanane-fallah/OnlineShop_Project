import random
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.utils import send_otp_code
from .decorators import unauthenticated_user
from django.utils.decorators import method_decorator
from .forms import CustomerCreationFrom, VerifyCodeForm
from .models import OptCode, User


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
        return redirect('index')


@method_decorator(unauthenticated_user, name='get')
class RegisterPage(View):
    form_class = CustomerCreationFrom
    template_name = 'account/register.html'
    def get(self, request):
        # form = CustomerCreationFrom()
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['mobile'], random_code)
            OptCode.objects.create(phone_number=form.cleaned_data['mobile'], code=random_code)
            request.session['user_info'] = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'username': form.cleaned_data['username'],
                'password1': form.cleaned_data['password1'],
                'password2': form.cleaned_data['password2'],
                'email': form.cleaned_data['email'],
                'mobile': form.cleaned_data['mobile'],
                'age': form.cleaned_data['age'],
            }
            messages.success(request, 'we send you a code')
            return redirect('account:verify')
        else:
            context = {
                'form': form
            }
            return render(request, self.template_name, context=context)


class UserVerify(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_info']
        code_ins = OptCode.objects.get(phone_number=user_session['mobile'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_ins.code:
                User.objects.create_user(first_name=user_session['first_name'],
                                         last_name=user_session['last_name'],
                                         username=user_session['username'],
                                         mobile=user_session['mobile'],
                                         email=user_session['email'],
                                         age=user_session['age'],
                                         password=user_session['password1'],

                                         )
                code_ins.delete()
                messages.success(request, 'register successfully', 'success')
                return redirect('account:login')
            else:
                messages.error(request, 'wrong code')
                return redirect('account:verify')
        return redirect('index')
