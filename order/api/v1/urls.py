from django.urls import path
from .views import *

urlpatterns = [
    path('cartdetail/', CartDetailList.as_view(), name='detail_create'),
    path('detail/<int:pk>/', CartItemDetail.as_view(), name='item_detail'),
    path('additem/', CartItemAddView.as_view(), name='add_item')
]