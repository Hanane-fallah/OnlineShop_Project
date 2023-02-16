from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/v1/', include('order.api.v1.urls')),
    path('cart/add/<str:product_name>/', ItemAddView.as_view(), name='item_add'),
    path('cartdetail/', CartView.as_view(), name='cart_detail'),
    path('cart/remove/<str:product_name>/', ItemRemoveView.as_view(), name='item_remove'),
    path('cart/create/', UserCartCreateView.as_view(), name='usercart_create'),
    path('cart/detail/', AddCartDetailView.as_view(), name='cartdetail_create'),
    path('usercart/', UserCartListView.as_view(), name='usercart_list'),
    path('addqty/<str:product>/', AddItemQtyView.as_view(), name='add_qty'),
    path('minusqty/<str:product>/', MinusItemQtyView.as_view(), name='minus_qty'),
    # path('detail/<uuid:cart_id>/', UserCartDetailView.as_view(), name='order_detail2')
]