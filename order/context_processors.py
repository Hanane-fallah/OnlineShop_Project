from .utils import CartSession


def cart(request):
    return {'cart': CartSession(request)}
