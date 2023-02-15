from django.shortcuts import render, get_object_or_404
from django.views import View
from product.models import Product
from .utils import CartSession
from .forms import CartAddForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserCart, CartItem, CartDetail


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
            'discount_price': cart.discount_price(),
            'final_price': cart.final_price()
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
        print('----------------------')
        if form.is_valid():
            cart.add(product, form.cleaned_data['qty'])
            print('---- add -----')
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


# todo: detailview
class UserCartDetailView(LoginRequiredMixin, View):
    def get(self, request, cart_id):
        cart = get_object_or_404(CartDetail, id=cart_id)
        return render(request, 'order/cart.html', {'cart': cart})


class UserCartCreateView(LoginRequiredMixin, View):
    """
    this view creates UserCart object for user in db
    & creates cart items in CartItem
    #  todo: add cart detail
    """

    def get(self, request):
        cart = CartSession(request)
        cart_obj = UserCart.objects.create(user_id=request.user)
        for item in cart:
            CartItem.objects.create(cart_id=cart_obj,
                                    product_id=item['name'],
                                    qty=item['qty']
                                    )

        cart.clear()
        return redirect('order:cart_detail')
