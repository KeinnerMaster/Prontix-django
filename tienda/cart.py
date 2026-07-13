from decimal import Decimal
from .models import Producto


CART_SESSION_KEY = 'carrito'


class Cart:
    """Carrito de compras guardado en la sesión del navegador.
    Estructura interna: { 'producto_id': {'cantidad': int, 'precio': str}, ... }
    """

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get(CART_SESSION_KEY)
        if not carrito:
            carrito = self.session[CART_SESSION_KEY] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] += cantidad
        else:
            self.carrito[producto_id] = {
                'cantidad': cantidad,
                'precio': str(producto.precio),
            }
        # Que la cantidad nunca supere el stock disponible
        if self.carrito[producto_id]['cantidad'] > producto.stock:
            self.carrito[producto_id]['cantidad'] = producto.stock
        self.guardar()

    def actualizar_cantidad(self, producto_id, cantidad):
        producto_id = str(producto_id)
        if producto_id in self.carrito and cantidad > 0:
            self.carrito[producto_id]['cantidad'] = cantidad
            self.guardar()
        elif producto_id in self.carrito and cantidad <= 0:
            self.eliminar(producto_id)

    def eliminar(self, producto_id):
        producto_id = str(producto_id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def vaciar(self):
        self.session[CART_SESSION_KEY] = {}
        self.guardar()

    def __iter__(self):
        """Recorre los items del carrito trayendo el producto real de la base
        de datos (para mostrar nombre, imagen, etc. en el template)."""
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        productos_map = {str(p.id): p for p in productos}

        for producto_id, item in self.carrito.items():
            producto = productos_map.get(producto_id)
            if not producto:
                continue
            precio = Decimal(item['precio'])
            cantidad = item['cantidad']
            yield {
                'producto': producto,
                'cantidad': cantidad,
                'precio_unitario': precio,
                'subtotal': precio * cantidad,
            }

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def total(self):
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.carrito.values()
        )
