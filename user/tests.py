from django.test import TestCase, Client
from .models import User, PayAccount
from django.urls import reverse


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        """
        here we create some test instances for our models
        :return: None
        """
        # user object
        a = User.objects.create(first_name='test-name',
                                last_name='test-last',
                                username='test-user',
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
        customer = User.objects.get(username='test-user')
        pay_acc = PayAccount.objects.get(account_number=1234123412341234)
        # if the objects are present in test database the following lines are True
        self.assertTrue(customer)
        self.assertTrue(pay_acc)


class LoginviewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='test-name',
                            last_name='test-last',
                            username='testuser2',
                            email='te@test.co',
                            age=24,
                            mobile='09909076129',
                            slug='test',
                            password='usertest1234'
                            )

    def setUp(self) -> None:
        self.client = Client()

    def test_user_login_GET(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        # self.failUnless(response.context['form'], CustomerCreationFrom)

    def test_user_login_POST_valid(self):
        response = self.client.post(reverse('account:login'), data={
            'username': 'testuser2',
            'password': 'usertest1234'
        })
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(User.objects.count(), 1)

    def test_user_login_POST_not_valid(self):
        response = self.client.post(reverse('account:login'), data={
            'username': 'tuser',
            'password': 'est1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login'))

    def logout_test(self):
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))


class RegisterviewTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_register_GET(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')
        # self.failUnless(response.context['form'], CustomerCreationFrom)

    def test_register_POST_valid(self):
        response = self.client.post(reverse('account:register'), data={
            'first_name': 'testname',
            'last_name': 'testlast',
            'username': 'testuser4',
            'email': 'tes4@test.co',
            'age': 24,
            'mobile': '09117654888',
            'password1': '1234akbarada',
            'password2': '1234akbarada'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:verify'))

    def test_register_POST_not_valid(self):
        response = self.client.post(reverse('account:register'), data={
            'first_name': 'testname',
            'last_name': 'testlast',
            'username': 'testuser4',
            'email': 'tes4',
            'age': 24,
            'mobile': '09888',
            'password1': '1234akbarada',
            'password2': '1234ada'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')


class UserVerifyTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_verify_GET(self):
        response = self.client.get(reverse('account:verify'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/verify.html')