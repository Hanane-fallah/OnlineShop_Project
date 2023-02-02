from django.test import TestCase
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

        UserCart.objects.create(user_id=a)


    def test_user_create(self):

        user_cart = UserCart.objects.get(user_id=1)

        self.assertTrue(user_cart)
