
from django.urls import path, re_path
from .views import Products, ShopCategories, ProductDetail

urlpatterns = [
    # path('', AdminIndex.as_view(), name='admin_index'),
    path('', Products.as_view(), name='all'),
    path('shop/', ShopCategories.as_view(), name='shop'),
    path('shop/<pk>', ProductDetail.as_view(), name='detail'),
    re_path(r'^(?P<slug>.*)/$', ShopCategories.as_view(), name='category'),
    # path('^shop/(?P<category>[a-zA-Z]+)/$', ShopCategories.as_view(), name='category'),
    # path('shop/chair/', ShopCategories.as_view(), name='category'),
    # path('login/', LoginPage.as_view(), name='login'),
    # path('logout/', LogoutPage.as_view(), name='logout'),

]