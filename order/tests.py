from django.test import TestCase
from product.models import PromotionType, Category
from .models import *


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        """
        here we create some test instances for our models
        :return: None
        """
        # customer object for usercart
        a = Customer.objects.create(first_name='test-name',
                                    last_name='test-last',
                                    user_name='test-user',
                                    email='test@test.co',
                                    age=24,
                                    mobile='09909009009',
                                    slug='test'
                                    )  # id = 1

        # user cart object
        uc = UserCart.objects.create(id='f377180a-aa2e-4799-bb2e-f55468e0f991', user_id=a)

        # shipping method test instance
        s = ShippingMethod.objects.create(name='test-shipping', price=10)

        # cart status test instance
        CartStatus.objects.create(status='test-status')

        # promotion type object
        c = PromotionType.objects.create(name='discount')
        # promotion object
        d = Promotion.objects.create(name='test-promo', type_id=c, value=20, hint='28', start_date='2023-02-02',
                                     end_date='2023-02-04')
        # cart detail instance for test usercart
        CartDetail.objects.create(
            cart_id=uc,
            order_date='2023-02-02',
            shipping_id=s,
            promotion_id=d,
            total_amount=100,
            entry=True
        )

        # test category instance for cart items
        cat = Category.objects.create(name='test-cat')
        # product test instance for cart items
        pr = Product.objects.create(name='test-product', category_id=cat, brand='test-brand', info='some info',
                                    price=2.2, qty=10, image='img/product/test.jpeg'
                                    )
        # test cart item
        CartItem.objects.create(cart_id=uc, product_id=pr, qty=5)

    def test_order_create(self):
        """
        here we queryset to get the instances created above
        :return: OK if all instances are present in test database
        """
        user_cart = UserCart.objects.get(user_id=1)
        shipping = ShippingMethod.objects.get(name='test-shipping')
        status = CartStatus.objects.get(status='test-status')
        detail = CartDetail.objects.get(cart_id='f377180a-aa2e-4799-bb2e-f55468e0f991')
        item = CartItem.objects.get(cart_id='f377180a-aa2e-4799-bb2e-f55468e0f991')
        # if the objects are present in test database the following lines are True
        self.assertTrue(user_cart)
        self.assertTrue(shipping)
        self.assertTrue(status)
        self.assertTrue(detail)
        self.assertTrue(item)
