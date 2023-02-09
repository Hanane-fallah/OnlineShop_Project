from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .managers import InProcessPromoManager
from user.models import expiry_date_validate, User


# VALIDATORS
def digit_validate(digit):
    '''
    check digit positive or not
    :param digit: entered number
    :return: None or
    :raise: ValidationError if digit is negative
    '''
    if digit <= 0:
        raise ValidationError(
            _('must be positive')
        )


# MODELS
class Category(models.Model):
    """
    define Category model for products

    ...

    Attributes
    ----------
    parent_cat : Category object
        self relation - each category can have one parent category or not ( main categories )
    name : str
        category's name
    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Category object.
    """
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='img/category', default='img/category/product5')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def children(self):
        children = Category.objects.filter(parent=self.id)
        return children

    def count_children(self):
        count_child = self.children().count()
        return count_child

    def products(self):
        child = self.children()
        products = Product.objects.filter(category_id__in=[c.id for c in child] + [self.id])
        return products

    def count_products(self):
        count_products = self.products().count()
        if count_products:
            return count_products
        else:
            return '--- No Product ---'


class Product(models.Model):
    """
    define Product model

    ...

    Attributes
    ----------
    name : str
        name of the product
    category_id : int
        foreign key to Category model instance ( define product category )
    brand : str
        product brand name
    info : str
        product details & info
    proce : float
        product price
    qty : int
        product stock
    image : str
        path to the product image in project media

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Product object.
    """
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=50)
    info = models.TextField(max_length=300)
    price = models.FloatField(validators=[digit_validate])
    qty = models.IntegerField(validators=[digit_validate])
    image = models.ImageField(upload_to='img/product')

    def __str__(self):
        return f'{self.name} : {self.qty}'

    def promo(self):
        try:
            promo_obj = InProcessPromo.objects.get(product_id=self)
            if promo_obj.in_process:
                return promo_obj.promotion_id

        except:
            return False

    def price_discount(self):
        try:
            if self.promo:
                promo = self.promo()
                if promo.type_id.name == 'cash':
                    if self.price > int(promo.hint):
                        return self.price - float(promo.value)
                elif promo.type_id.name == 'percentage':
                    discount = self.price * float(promo.value)
                    if discount < int(promo.hint):
                        return self.price - discount
        except (AttributeError, ValueError):
            return False


class PromotionType(models.Model):
    """
    define Promotion types for the website

    ...

    Attributes
    ----------
    name : str
        name of the promotion type

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of PromotionType object.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Promotion(models.Model):
    """
    define Promotion model

    ...

    Attributes
    ----------
    name : str
        name of the promotion
    type_id : int
        foreign key to PromotionType model instance ( define promotion type )
    value : float
        promotion value( in % or $ )
    hint : str
        in percentage -> maximum promotion & in cash -> minimum & in cart promo -> Discount phrase
    start_date : date
        start date of promotion
    end_date : date
        end date of promotion

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Promotion object.
    """
    name = models.CharField(max_length=50, unique=True)
    type_id = models.ForeignKey(PromotionType, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    hint = models.CharField(max_length=50)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=False, validators=[expiry_date_validate])

    def __str__(self):
        return f'{self.name} : {self.value}'


class InProcessPromo(models.Model):
    """
    model for inprocess promotions

    ...

    Attributes
    ----------
    product_id : int
        foreign key to Product model instance
    promotion_id : int
        foreign key to Promotion model instance
    in_process : bool
        True if promotion is in-process, otherwise False

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of InProcessPromo object.
    """
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    promotion_id = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    in_process = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.promotion_id} - {self.product_id}'

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        promo_end = self.promotion_id.end_date
        if expiry_date_validate(promo_end):
            if not InProcessPromo.objects.filter(product=self.product, in_process=True).exists():
                super().save()
            else:
                raise ValidationError(
                    _('This Product already has offer')
                )
        else:
            raise ValidationError(
                _('This promo is expired')
            )


class Review(models.Model):
    """
    model for Review of products

    ...

    Attributes
    ----------
    user_id : user object
        foreign key to user model ( to define review owner )
    product_id : int
        foreign key to Product model instance ( define related product )
    rating : str
        number from 1-5 to define rating stars of product
    comment : str
        user comment is stored in this field

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Review object.
    """
    RATING = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING)
    comment = models.TextField(max_length=600)

    def __str__(self):
        return f'* {self.rating} * : {self.comment}'
