from product.models import Product

CART_SESSION_ID = 'cart'


class CartSession:
    def __init__(self, request):
        self.session = request.session
        # cart = self.session.get(CART_SESSION_ID) or self.session[CART_SESSION_ID]
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_names = self.cart.keys()
        products = Product.objects.filter(name__in=product_names)
        # total = sum(p.final_price() for p in products)
        # self.cart['cart_total_price'] = total
        cart = self.cart.copy()
        for item in self.cart.values():
            # item['total_price'] = float(item['price']) * item['qty']
            # self.cart_total_price += float(item['final_price'])
            yield item

        # self.total_price()

    def __len__(self):
        return len(self.cart.keys())

    def add(self, product, qty):
        product_id = str(product.name)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'qty': 0, 'price': product.price,
                'name': product.name, 'img': product.image.url,
                'price_discount': product.price_discount() or 0,
                'final_price': product.final_price()
            }
        self.cart[product_id]['qty'] += qty
        self.total_price()
        self.save()

    def remove(self, product):
        produc_name = str(product.name)
        if produc_name in self.cart:
            del self.cart[produc_name]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def total_price(self):
        product_names = self.cart.keys()
        total = sum(self.cart[p]['price']*self.cart[p]['qty'] for p in product_names)
        return total.__round__(2)

    def cart_discount_price(self):
        return self.total_price() - self.cart_final_price()

    def cart_final_price(self):
        product_names = self.cart.keys()
        # print(product_names)
        # total = (self.cart[p]['final_price'] for p in product_names)
        # for a in total:
        #     print(type(a), '---', a)
        # return total
        total = sum(self.cart[p]['final_price'] * self.cart[p]['qty'] for p in product_names)
        return total.__round__(2)