from django.test import TestCase

from product.models import PromotionType, Category
from .models import *


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        a = Customer.objects.create(first_name='test-name',
                                    last_name='test-last',
                                    user_name='test-user',
                                    email='test@test.co',
                                    age=24,
                                    mobile='09909009009',
                                    slug='test'
                                    )  # id = 1

        uc = UserCart.objects.create(id='f377180a-aa2e-4799-bb2e-f55468e0f991', user_id=a)

        s = ShippingMethod.objects.create(name='test-shipping', price=10)

        CartStatus.objects.create(status='test-status')

        p = PayAccount.objects.create(user_id=a, account_number=1234123412341234, expiry_date='2023-04-04',
                                      is_default=True)
        c = PromotionType.objects.create(name='discount')
        d = Promotion.objects.create(name='test-promo', type_id=c, value=20, hint='28', start_date='2023-02-02',
                                     end_date='2023-02-04')
        CartDetail.objects.create(
            cart_id=uc,
            order_date='2023-02-02',
            pay_account_id=p,
            shipping_id=s,
            promotion_id=d,
            total_amount=100,
            entry=True
        )

        cat = Category.objects.create(name='test-cat')
        pr = Product.objects.create(name='test-product', category_id=cat, brand='test-brand', info='some info',
                                   price=2.2, qty=10, image='img/product/test.jpeg'
                                   )
        CartItem.objects.create(cart_id=uc, product_id=pr, qty=5)

    def test_order_create(self):
        user_cart = UserCart.objects.get(user_id=1)
        shipping = ShippingMethod.objects.get(name='test-shipping')
        status = CartStatus.objects.get(status='test-status')
        detail = CartDetail.objects.get(cart_id='f377180a-aa2e-4799-bb2e-f55468e0f991')
        item = CartItem.objects.get(cart_id='f377180a-aa2e-4799-bb2e-f55468e0f991')

        self.assertTrue(user_cart)
        self.assertTrue(shipping)
        self.assertTrue(status)
        self.assertTrue(detail)
        self.assertTrue(item)
