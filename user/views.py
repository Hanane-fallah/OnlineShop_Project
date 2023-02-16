import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth import views as auth_view
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from core.utils import send_otp_code
from .decorators import unauthenticated_user
from django.utils.decorators import method_decorator
from .forms import CustomerCreationFrom, VerifyCodeForm
from .models import OtpCode, User, Address
from django.contrib.auth.forms import PasswordChangeForm


@method_decorator(unauthenticated_user, name='get')
class LoginPage(View):
    """
    Login view for users
    and link to admin login

    ...

    Methods
    -------
    get:
        sends login page html
    post:
        gets user's username & pass
        authenticate user
        :return home page
    """

    def get(self, request):

        return render(request, 'account/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj:
            login(request, user_obj)
            messages.success(request, 'user loged in successfully')
            if user_obj.is_staff:
                return redirect('admin:index')
        else:
            messages.info(request, 'username or pass incorrect')
        return redirect('account:login')


class LogoutPage(View):
    """
    Logout view for users

    ...

    Methods
    -------
    get:
        logout user and redirect to home page

    """

    def get(self, request):
        logout(request)
        return redirect('index')


@method_decorator(unauthenticated_user, name='get')
class RegisterPage(View):
    """
    Register view for users

    ...

    Methods
    -------
    get:
        send register page and form
    post:
        get & check data from form & send sms to user mobile
        :return to verify page
        wrong data: send register page again

    """
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
            OtpCode.objects.create(phone_number=form.cleaned_data['mobile'], code=random_code)
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
    """
    Verify User with OPT CODE

    ...

    Methods
    -------
    get:
        send verify page and form
    post:
        check code and register user if valid
        :return to login page
        :wrong data send verify page again
        :else gome page

    """
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_info']
        code_ins = OtpCode.objects.get(phone_number=user_session['mobile'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_ins.code:
                user = User.objects.create_user(first_name=user_session['first_name'],
                                                last_name=user_session['last_name'],
                                                username=user_session['username'],
                                                mobile=user_session['mobile'],
                                                email=user_session['email'],
                                                age=user_session['age'],
                                                password=user_session['password1'],

                                                )

                login(request, user)
                code_ins.delete()
                messages.success(request, 'register successfully', 'success')
                return redirect('index')
            else:
                messages.error(request, 'wrong code')
                return redirect('account:verify')
        return redirect('account:register')


class UserPasswordReset(auth_view.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDone(auth_view.PasswordResetDoneView):
    template_name = 'account/password_reset_Done.html'


class PasswordResetConfirm(auth_view.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class PasswordResetComplete(auth_view.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/user_detail.html'


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'age', 'mobile', 'username']
    template_name = 'account/user_update_form.html'

    def get_success_url(self):
        return reverse_lazy('account:user_profile', kwargs={'slug': self.kwargs['slug']})


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'account/change_password.html'

    def get_success_url(self):
        return reverse_lazy('account:user_profile', kwargs={'slug': self.kwargs['slug']})


class SetDefaultAddress(LoginRequiredMixin, View):
    def get(self, request, old_ad, new_ad):
        old_address = Address.objects.get(id=old_ad)
        old_address.is_default = False
        new_address = Address.objects.get(id=new_ad)
        new_address.is_default = True
        old_address.save()
        new_address.save()
        return redirect(request.META.get('HTTP_REFERER'))

