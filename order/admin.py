from django.contrib import admin

from order.models import *

admin.site.register(UserCart)
admin.site.register(ShippingMethod)
admin.site.register(CartStatus)
