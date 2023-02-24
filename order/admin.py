from django.contrib import admin

from order.models import UserCart, ShippingMethod, CartStatus, CartDetail, CartItem


class CartIteminLine(admin.TabularInline):
    model = CartItem
    raw_id_fields = ('product',)


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'entry')
    list_filter = ('entry',)
    search_fields = ('user_id', 'id')
    inlines = (CartIteminLine, )


@admin.register(ShippingMethod)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(CartStatus)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)
    ordering = ('status',)


@admin.register(CartDetail)
class CartDetailAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'order_date',)
    list_filter = ('order_date', 'shipping_id', 'promotion_id',)
    fieldsets = (
        ('Main info', {'fields': ('cart_id', 'order_date', 'total_amount','status')}),
        ('more info', {'fields': ('shipping_id', 'promotion_id')}),
    )

    search_fields = ('cart_id',)
    ordering = ('order_date',)


@admin.register(CartItem)
class CartitemAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'product_id', 'qty',)
    list_filter = ('product_id',)
    search_fields = ('cart_id', 'product_id')
    ordering = ('cart_id',)

