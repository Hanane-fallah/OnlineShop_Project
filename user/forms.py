from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomerCreationFrom(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile', 'age')
