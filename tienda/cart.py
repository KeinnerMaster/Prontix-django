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

    def agregar(self, producto, cantidad=1, variante_id=None):
        # Usamos una clave compuesta (producto + variante) para que
        # "Camiseta Talla M" y "Camiseta Talla L" sean items distintos en el carrito
        clave = f"{producto.id}_{variante_id}" if variante_id else str(producto.id)

        if clave in self.carrito:
            self.carrito[clave]['cantidad'] += cantidad
        else:
            self.carrito[clave] = {
                'producto_id': producto.id,
                'variante_id': variante_id,
                'cantidad': cantidad,
                'precio': str(producto.precio),
            }

        max_stock = producto.stock
        if variante_id:
            variante = producto.variantes.filter(id=variante_id).first()
            if variante:
                max_stock = variante.stock

        if self.carrito[clave]['cantidad'] > max_stock:
            self.carrito[clave]['cantidad'] = max_stock
        self.guardar()

    def actualizar_cantidad(self, clave, cantidad):
        clave = str(clave)
        if clave in self.carrito and cantidad > 0:
            self.carrito[clave]['cantidad'] = cantidad
            self.guardar()
        elif clave in self.carrito and cantidad <= 0:
            self.eliminar(clave)

    def eliminar(self, clave):
        clave = str(clave)
        if clave in self.carrito:
            del self.carrito[clave]
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def vaciar(self):
        self.session[CART_SESSION_KEY] = {}
        self.guardar()

    def __iter__(self):
        """Recorre los items del carrito trayendo el producto (y la variante,
        si aplica) reales de la base de datos."""
        producto_ids = [item['producto_id'] for item in self.carrito.values()]
        productos = Producto.objects.filter(id__in=producto_ids)
        productos_map = {p.id: p for p in productos}

        for clave, item in self.carrito.items():
            producto = productos_map.get(item['producto_id'])
            if not producto:
                continue

            variante = None
            if item.get('variante_id'):
                variante = producto.variantes.filter(id=item['variante_id']).first()

            precio = Decimal(item['precio'])
            cantidad = item['cantidad']
            yield {
                'clave': clave,
                'producto': producto,
                'variante': variante,
                'cantidad': cantidad,
                'precio_unitario': precio,
                'subtotal': precio * cantidad,
            }

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def total_sin_descuento(self):
        return sum(
            Decimal(item['precio']) * item['cantidad']
            for item in self.carrito.values()
        )

    def aplicar_cupon(self, codigo):
        from .models import Cupon
        try:
            cupon = Cupon.objects.get(codigo__iexact=codigo)
        except Cupon.DoesNotExist:
            return False, "Cupom não encontrado."

        valido, mensaje = cupon.es_valido(self.total_sin_descuento())
        if not valido:
            return False, mensaje

        self.session['cupon_codigo'] = cupon.codigo
        self.guardar()
        return True, f"Cupom {cupon.codigo} aplicado com sucesso!"

    def quitar_cupon(self):
        if 'cupon_codigo' in self.session:
            del self.session['cupon_codigo']
            self.guardar()

    def get_cupon(self):
        from .models import Cupon
        codigo = self.session.get('cupon_codigo')
        if not codigo:
            return None
        try:
            return Cupon.objects.get(codigo__iexact=codigo)
        except Cupon.DoesNotExist:
            return None

    def descuento(self):
        cupon = self.get_cupon()
        if not cupon:
            return Decimal('0')
        valido, _ = cupon.es_valido(self.total_sin_descuento())
        if not valido:
            return Decimal('0')
        return cupon.calcular_descuento(self.total_sin_descuento())

    def total(self):
        return max(Decimal('0'), self.total_sin_descuento() - self.descuento())
