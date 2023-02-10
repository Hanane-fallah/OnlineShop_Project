from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from user.decorators import admin_user
from product.models import Product, Category


@method_decorator(admin_user, name='get')
class IndexCategories(ListView):
    """
    this view shows landing page of website
    all categories with image are presenting here
    """
    model = Category
    template_name = 'product/index.html'


@method_decorator(admin_user, name='get')
class ShopCategories(ListView):
    """
    this view shows shop page of website
    all products with image are presenting here
    if a category is choosen , products of that category are showing
    """
    model = Category
    template_name = 'product/shop.html'
    context_object_name = 'category_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        """
        here we check url, if it has slug , witch is category name
        it filters products to show that category products
        :param kwargs: request data
        :return: all products if slug=none,
        :else: category and subcategories (if existed) products
        """
        context = super().get_context_data(**kwargs)

        if 'slug' in self.kwargs:
            category = Category.objects.get(name=self.kwargs['slug'])
            context['products'] = category.products()
        else:
            context['products'] = Product.objects.all()

        return context


@method_decorator(admin_user, name='get')
class ProductDetail(DetailView):
    """
    this view shows product detail
    and order link
    """
    model = Product


