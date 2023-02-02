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

        city = City.objects.create(name='sample-city')

        Address.objects.create(user_id=a,
                               city_id=city,
                               street='sample-street',
                               postal_code='999999999',
                               detail='some extra detail',
                               is_default=True
                               )

        PayAccount.objects.create(
            user_id=a,
            account_number=1234123412341234,
            expiry_date='2023-04-04',
            is_default=True
        )

    def test_user_create(self):
        customer = Customer.objects.get(user_name='test-user')
        address = Address.objects.get(detail='some extra detail')
        pay_acc = PayAccount.objects.get(account_number=1234123412341234)
        # print('ad ', address)
        self.assertTrue(customer)
        self.assertTrue(address)
        self.assertTrue(pay_acc)

