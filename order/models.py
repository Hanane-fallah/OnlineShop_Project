import uuid
from django.db import models
from product.models import Promotion, Product
from user.models import Customer


# VALIDATORS

# MODELS
class UserCart(models.Model):
    """
    model for Customer's Shopping Cart

    ...

    Attributes
    ----------
    id : str
        generating uuid for each cart ( as primary key )
    user_id : customer object
        foreign key to customer model ( to define cart owner )

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Cart object.
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} : {self.id}'


class ShippingMethod(models.Model):
    """
    model for website's Shipping method

    ...

    Attributes
    ----------
    name : str
        name of the shipping way
    price : float
        price of shipping

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of Shipping object.
    """
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} - {self.price} $'


class CartStatus(models.Model):
    """
    model for Shopping Cart Statuses

    ...

    Attributes
    ----------
    status : str
        define status for cart

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of CartStatus object.
    """
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status


class CartDetail(models.Model):
    """
    model for Shopping Cart Detail

    ...

    Attributes
    ----------
    cart_id : str
        foreign key to Cart model ( connect cart to cart detail )
    order_date : date
        cart register date ( will be added when customer register and pay the cart )
    shipping_id : int
        foreign key to Shipping model
    promotion_id : int
        foreign key to Promotion model ( id customer has a promotion hint for cart )
    total_amount : float
        final total amount of cart to pay
    entry : bool
        True if customer registered & closed cart, otherwise False

    Methods
    -------
    save:
        save the object in database
    str:
        string representation of CartDetail object.
    """

    cart_id = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    order_date = models.DateField(null=True, blank=True)
    shipping_id = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    promotion_id = models.ForeignKey(Promotion, on_delete=models.DO_NOTHING, null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    entry = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cart_id} - {self.order_date} : {self.total_amount} $ - {self.entry}'


class CartItem(models.Model):
    """
    model for Shopping Cart Items

    ...

    Attributes
    ----------
    cart_id : str
        foreign key to Cart model ( connect cart to its items )
    product_id : int
        foreign key to Product model instance ( connect cart to product )
    qty : int
        ordered qty of product

    Methods
    -------
    save:
        checks product qty and if available will save the cart item in database
    str:
        string representation of Cart object.
    """
    cart_id = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        overriding save cart item method to check product qty
        if the cart item qty is more than product qty the item is not registered
        :param force_insert, force_update, using, update_fields: django default params
        :return: None
        :raise: Exception if Insufficient inventory
        """
        if self.qty <= self.product_id.qty:
            super().save()
        else:
            raise Exception("Insufficient inventory")

    def __str__(self):
        return f'{self.product_id} ^ {self.qty}'
