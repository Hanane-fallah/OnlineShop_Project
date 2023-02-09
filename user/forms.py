from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from .models import User
from django import forms


class CustomerCreationFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile', 'age')


class CustomerChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='You can change password <a href=\'../password/\'>here</a>')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'mobile', 'age')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

