from django.views.generic import TemplateView, ListView

from product.models import Product, Category


# class Index(TemplateView):
#     template_name = 'product/index.html'


class Products(ListView):
    model = Product
    paginate_by = 5


class IndexCategories(ListView):
    model = Category
    template_name = 'product/index.html'


class ProductCategories(ListView):
    model = Category
    template_name = 'product/shop.html'
