from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from product.models import Category, Product, Promotion, PromotionType, InProcessPromo, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'children_categories', 'cat_products')
    list_filter = ('parent',)

    def parent_category(self, obj):
        if obj.parent:
            return obj.parent
        else:
            return '--- Main ---'

    def children_categories(self, obj):
        return obj.count_children()

    def cat_products(self, obj):
        return obj.count_products()

    fieldsets = (
        ('Main info', {'fields': ('name', 'parent', 'image')}),

    )

    add_fieldsets = (
        (None, {'fields': ('name', 'parent')})
    )
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'stock')
    list_filter = ('category_id', 'brand',)

    def stock(self, obj):
        if obj.qty < 1:
            return '-- unavailable --'
        else:
            return obj.qty

    fieldsets = (
        ('Main info', {'fields': ('name', 'category_id', 'brand', 'qty', 'slug')}),
        ('More info', {'fields': ('price', 'info', 'image')}),

    )

    search_fields = ('name', 'brand')
    ordering = ('name',)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_id', 'value',)
    list_filter = ('type_id', 'value', 'start_date', 'end_date')

    fieldsets = (
        ('Main info', {'fields': ('name', 'type_id', 'value', 'hint')}),
        ('Active date', {'fields': ('start_date', 'end_date')}),

    )

    search_fields = ('name',)
    ordering = ('name',)


@admin.register(InProcessPromo)
class InProcessPromotionAdmin(admin.ModelAdmin):
    list_display = ('product', 'promotion_id', 'in_process',)
    list_filter = ('in_process', 'promotion_id',)

    search_fields = ('product_id',)
    ordering = ('product_id',)


@admin.register(PromotionType)
class PromotionTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('rating', 'user_id', 'comment', 'product')
    list_filter = ('rating',)

    def product(self, obj):
        url = (
            reverse("admin:product_product_change", args=str(obj.product_id.id))

        )
        return format_html('<a href="{}">{}</a>', url, obj.product_id)

    fieldsets = (
        ('Rate info', {'fields': ('rating', 'comment', 'user_id', 'product_id')}),

    )

    add_fieldsets = (
        ('New comment', {'fields': ('rating', 'comment', 'user_id', 'product_id')})
    )
    search_fields = ('product',)
    ordering = ('rating',)
