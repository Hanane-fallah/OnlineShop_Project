from django.contrib import admin

from product.models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Promotion)
admin.site.register(PromotionType)
admin.site.register(InProcessPromo)
admin.site.register(Review)
