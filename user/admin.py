from django.contrib import admin

from user.models import *

admin.site.register(Customer)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(PayAccount)

