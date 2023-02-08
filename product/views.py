from django.views.generic import TemplateView, ListView

from product.models import Product, Category


# class Index(TemplateView):
#     template_name = 'product/index.html'


class Products(ListView):
    model = Product
    paginate_by = 6


class IndexCategories(ListView):
    model = Category
    template_name = 'product/index.html'


class ShopCategories(ListView):
    model = Category
    template_name = 'product/shop.html'
    context_object_name = 'category_list'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'slug' in self.kwargs:
            category = Category.objects.get(name=self.kwargs['slug'])
            context['products'] = category.products()
        else:
            context['products'] = Product.objects.all()

        return context
