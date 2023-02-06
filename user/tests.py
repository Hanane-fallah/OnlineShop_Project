from django.test import TestCase
from .models import *
from iranian_cities.models import Ostan, Shahrestan


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        """
        here we create some test instances for our models
        :return: None
        """
        # user object
        a = User.objects.create(first_name='test-name',
                                last_name='test-last',
                                user_name='test-user',
                                email='test@test.co',
                                age=24,
                                mobile='09909009009',
                                slug='test'
                                )
        # pay account object
        PayAccount.objects.create(
            user_id=a,
            account_number=1234123412341234,
            expiry_date='2023-04-04',
            is_default=True
        )

    def test_user_create(self):
        """
        here we queryset to get the instances created above
        :return: OK if all instances are present in test database
        """
        customer = User.objects.get(user_name='test-user')
        pay_acc = PayAccount.objects.get(account_number=1234123412341234)
        # if the objects are present in test database the following lines are True
        self.assertTrue(customer)
        self.assertTrue(pay_acc)
