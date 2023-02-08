
from django.urls import path
from .views import Products, ProductCategories


urlpatterns = [
    # path('', AdminIndex.as_view(), name='admin_index'),
    path('', Products.as_view(), name='all'),
    path('shop/', ProductCategories.as_view(), name='shop'),
    # path('login/', LoginPage.as_view(), name='login'),
    # path('logout/', LogoutPage.as_view(), name='logout'),

]
# ]