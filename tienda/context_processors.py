from .cart import Cart


def cart_count(request):
    carrito = Cart(request)
    return {'cart_count': len(carrito)}
