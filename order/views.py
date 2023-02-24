from datetime import date

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import View
from product.models import Product
from .utils import CartSession
from .forms import CartAddForm, CartDetailForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserCart, CartItem, CartDetail, ShippingMethod


class CartView(View):
    """
    showing user cart info with request session data
    """

    def get(self, request):
        """
        using request ro access session cart values ( with SessionCart utils )
        :return:
        """
        cart = CartSession(request)
        context = {
            'cart': cart,
            'total_amount': cart.total_price(),
            'discount_price': cart.cart_discount_price(),
            'final_price': cart.cart_final_price(),
            'shipping': ShippingMethod.objects.all(),
        }

        return render(request, 'order/cart.html', context)


class ItemAddView(View):
    """
    this view is for add to cart button
    uses request session to store cart item values in cart session
    """

    def post(self, request, product_name):
        cart = CartSession(request)
        product = get_object_or_404(Product, name=product_name)
        form = CartAddForm(request.POST)

        if form.is_valid():
            # checks product stock with ordered qty
            if product.qty >= form.cleaned_data['qty']:
                cart.add(product, form.cleaned_data['qty'])
                product.qty -= form.cleaned_data['qty']
                product.save()
            else:
                messages.info(request, 'insufficient quantity :(')
        #  redirect to remain on the current page
        return redirect(request.META.get('HTTP_REFERER'))


class ItemRemoveView(View):
    """
    this view deletes items from cart ( in request session )
    """

    def get(self, request, product_name):
        cart = CartSession(request)
        # product = get_object_or_404(Product, name=product_name)
        # cart.remove(product)
        cart.remove(product_name)
        return redirect('order:cart_detail')


class UserCartCreateView(LoginRequiredMixin, View):
    """
    this view creates UserCart object for user in db
    & creates cart items in CartItem
    """

    def get(self, request):
        cart = CartSession(request)
        usercart = UserCart.user_open_cart(request.user)
        usercart_id = usercart.id
        for item in cart:
            CartItem.objects.create(cart_id_id=usercart_id,
                                    product_id=item['name'],
                                    qty=item['qty']
                                    )

        cart.clear()
        usercart.entry = True
        usercart.save()
        return redirect('order:usercart_list')


class AddCartDetailView(LoginRequiredMixin, View):
    """
    this view gets cart detail value & add to db
    create CartDetail object
    :redirect ro add cart item view(UserCartCreateView)
    """

    def post(self, request):
        form = CartDetailForm(request.POST)
        if form.is_valid():
            cart_id = UserCart.user_open_cart(request.user).id
            order_date = date.today()
            shipping_name = form.cleaned_data['shipping']
            shipping_obj = ShippingMethod.objects.get(name=shipping_name)
            shipping_price = shipping_obj.price
            total_amount = form.cleaned_data['total_amount'] + shipping_price
            CartDetail.objects.create(cart_id_id=cart_id, order_date=order_date, shipping_id=shipping_obj,
                                      total_amount=total_amount)

        return redirect('order:usercart_create')
        # return redirect('order:cart_detail')


class UserCartListView(LoginRequiredMixin, View):
    """
    this view filters user's carts that are checked out (entry = True)
    """

    def get(self, request):
        carts = UserCart.objects.filter(user_id=request.user)
        return render(request, 'order/cart_list.html', {'carts': carts})


class AddItemQtyView(View):
    def get(self, request, product):
        cart = CartSession(request)
        cart.add_qty(product)
        return redirect('order:cart_detail')


class MinusItemQtyView(View):
    def get(self, request, product):
        cart = CartSession(request)
        cart.minus_qty(product)
        return redirect('order:cart_detail')


from rest_framework.reverse import reverse
import requests as client
DOMAIN = "http://127.0.0.1:8000"
class ApiAddItem(View):
    def get(self, request):
        cart = CartSession(request)
        usercart = UserCart.user_open_cart(request.user)
        usercart_id = usercart.id
        endpoint = reverse('order:item_list')
        for item in cart:
            product = Product.objects.get(name=item['name'])
            a = client.post(f"{DOMAIN}{endpoint}", data={
                'cart_id': usercart,
                'product': product,
                'qty': item['qty']
            })
            # print(a.data)
            # CartItem.objects.create(cart_id_id=usercart_id,
            #                         product_id=item['name'],
            #                         qty=item['qty']
            #                         )

        cart.clear()
        usercart.entry = True
        usercart.save()
        return redirect('order:usercart_list')