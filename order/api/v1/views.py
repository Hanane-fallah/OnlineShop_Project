from datetime import date
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from product.models import Product
from .serializers import CartDetailSerializer, CartItemSerializer, ProductSerializer, CartItemFormSerializer
from rest_framework.views import APIView

from ...models import CartItem, CartDetail, UserCart, ShippingMethod

data = {
    'id': 24,
    'title': "my dear",
}


class CartDetailList(APIView):
    def post(self, request, *args, **kwargs):
        cart_id = UserCart.user_open_cart(request.user)
        order_date = date.today()
        shipping_name = request.data['shipping']
        shipping_obj = ShippingMethod.objects.get(name=shipping_name)
        shipping_price = shipping_obj.price
        total_amount = float(request.data['total_amount']) + shipping_price
        serializer = CartDetailSerializer(data={
            'cart_id': cart_id,
            'order_date': order_date,
            'shipping_id': shipping_obj,
            'total_amount': total_amount
        })
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class CartItemDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = CartDetail.objects.all()
    serializer_class = CartDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CartItemAddView(mixins.CreateModelMixin,
                      generics.GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        product = request.POST['product']
        print('product', product)
        qty = request.POST['qty']
        cart_id = UserCart.user_open_cart(request.user).id
        serializer = CartItemFormSerializer(data={
            'product_name': product,
            'qty': int(qty),
            'cart_id': cart_id,
        })
        if serializer.is_valid():
            product = Product.objects.get(slug=product)
            qty = int(request.POST['qty'])
            cart_id = UserCart.user_open_cart(request.user)
            CartItem.objects.create(product=product, qty=qty, cart_id=cart_id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)
