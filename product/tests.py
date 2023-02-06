from django.test import TestCase
from .models import *


class ModelsTestCase(TestCase):
    def setUp(self) -> None:
        """
        here we create some test instances for our models
        :return: None
        """
        # main category object
        a = Category.objects.create(name='test-cat')

        # child category object
        Category.objects.create(parent_cat=a, name='test-child-cat')

        # product object for in process promos
        b = Product.objects.create(
            name='test-product',
            category_id=a,
            brand='test-brand',
            info='some info',
            price=2.2,
            qty=10,
            image='img/product/test.jpeg'
        )

        # promotion type object
        c = PromotionType.objects.create(name='discount')

        # promotion object
        d = Promotion.objects.create(
            name='test-promo',
            type_id=c,
            value=20,
            hint='28',
            start_date='2023-02-02',
            end_date='2023-02-04',
        )
        print('promotion', d.id)
        print('promotion---', b.id)

        # in=process promotion object
        InProcessPromo.objects.create(product_id=b, promotion_id=d, in_process=True)

        # cutomer object for review
        u = User.objects.create(first_name='test-name',
                                last_name='test-last',
                                user_name='test-user',
                                email='test@test.co',
                                age=24,
                                mobile='09909009009',
                                slug='test'
                                )  # id = 1
        # review object
        Review.objects.create(user_id=u, product_id=b, rating='3', comment='some comments')

    def test_product_create(self):
        """
        here we queryset to get the instances created above
        :return: OK if all instances are present in test database
        """
        cat_1 = Category.objects.get(name='test-cat')
        cat_2 = Category.objects.get(name='test-child-cat')
        product = Product.objects.get(name='test-product')
        promo_type = PromotionType.objects.get(name='discount')
        promo = Promotion.objects.get(name='test-promo')
        inprocess_promo = InProcessPromo.objects.get(product_id=2, promotion_id=2, in_process=True)
        review = Review.objects.get(user_id=2, product_id=2, rating='3', comment='some comments')
        # if the objects are present in test database the following lines are True
        self.assertTrue(cat_1)
        self.assertTrue(cat_2)
        self.assertTrue(product)
        self.assertTrue(promo_type)
        self.assertTrue(promo)
        self.assertTrue(inprocess_promo)
        self.assertTrue(review)
