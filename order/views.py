from datetime import date

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
            cart.add(product, form.cleaned_data['qty'])
        #  redirect to remain on the current page
        return redirect(request.META.get('HTTP_REFERER'))


class ItemRemoveView(View):
    """
    this view deletes items from cart ( in request session )
    """

    def get(self, request, product_name):
        cart = CartSession(request)
        product = get_object_or_404(Product, name=product_name)
        cart.remove(product)
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
        return redirect('order:cart_detail')


class AddCartDetailView(LoginRequiredMixin, View):
    """
    this view gets cart detail value & add to db
    create CartDetail object
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
            CartDetail.objects.create(cart_id_id=cart_id, order_date=order_date, shipping_id=shipping_obj, total_amount=total_amount)

        return redirect('order:usercart_create')
        # return redirect('order:cart_detail')


class UserCartListView(LoginRequiredMixin, View):
    def get(self, request):
        carts = UserCart.objects.filter(user_id=request.user)
        return render(request, 'order/cart_list.html', {'carts': carts})
