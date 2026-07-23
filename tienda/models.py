from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    destacado = models.BooleanField(default=False, help_text="Mostrar en la página principal")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class Variante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    talla = models.CharField(max_length=20, blank=True, help_text="Ej: S, M, L, 38, 39, 40 (dejar vacío si no aplica)")
    color = models.CharField(max_length=50, blank=True, help_text="Ej: Rojo, Negro (dejar vacío si no aplica)")
    stock = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Variantes"

    def __str__(self):
        partes = [p for p in [self.talla, self.color] if p]
        detalle = " / ".join(partes) if partes else "Única"
        return f"{self.producto.nombre} - {detalle}"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cupon = models.ForeignKey('Cupon', on_delete=models.SET_NULL, null=True, blank=True)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nombre_cliente = models.CharField(max_length=200)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=30)
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    notas = models.TextField(blank=True, help_text="Instrucciones adicionales del cliente (opcional)")

    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Pedidos"
        ordering = ['-creado_en']

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    nombre_producto = models.CharField(max_length=200)  # copia por si el producto se borra después
    variante_info = models.CharField(max_length=100, blank=True, help_text="Ej: Tamanho M / Cor Azul")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_producto}"

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes_adicionales')
    imagen = models.ImageField(upload_to='productos/galeria/')
    orden = models.PositiveIntegerField(default=0, help_text="Orden de aparición (menor número = primero)")

    class Meta:
        verbose_name_plural = "Imágenes de producto"
        ordering = ['orden']

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class ConfiguracionSitio(models.Model):
    modo_mantenimiento = models.BooleanField(default=False, help_text="Si está activo, los visitantes verán una página de mantenimiento")
    mensaje_mantenimiento = models.TextField(
        default="Estamos realizando mejoras. Voltamos em breve!",
        help_text="Mensaje que verán los visitantes durante el mantenimiento"
    )

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"

    def __str__(self):
        return "Configuración del sitio"

    def save(self, *args, **kwargs):
        # Aseguramos que solo exista 1 registro de configuración
        self.pk = 1
        super().save(*args, **kwargs)

class Cliente(models.Model):
    CLASIFICACION_CHOICES = [
        ('lead', 'Lead (Potencial)'),
        ('activo', 'Cliente Ativo'),
        ('inactivo', 'Cliente Inativo'),
    ]

    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30, blank=True)
    clasificacion = models.CharField(max_length=20, choices=CLASIFICACION_CHOICES, default='lead')
    total_gastado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad_pedidos = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True, help_text="Notas internas sobre este cliente")

    class Meta:
        verbose_name_plural = "Clientes"
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} ({self.email})"


class SuscriptorNewsletter(models.Model):
    email = models.EmailField(unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Suscriptores Newsletter"
        ordering = ['-creado_en']

    def __str__(self):
        return self.email

class Cupon(models.Model):
    TIPO_CHOICES = [
        ('porcentaje', 'Porcentagem (%)'),
        ('fijo', 'Valor fixo (R$)'),
    ]

    codigo = models.CharField(max_length=50, unique=True, help_text="Ej: HOCCE10, BLACKFRIDAY")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='porcentaje')
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Si es porcentaje: 10 = 10%. Si es fijo: 15 = R$15,00")
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    usos_maximos = models.PositiveIntegerField(default=1, help_text="Cuántas veces se puede usar este cupón en total")
    usos_actuales = models.PositiveIntegerField(default=0, editable=False)
    compra_minima = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Monto mínimo de compra para poder usarlo (0 = sin mínimo)")

    class Meta:
        verbose_name_plural = "Cupones"

    def __str__(self):
        return self.codigo.upper()

    def es_valido(self, total_carrito=0):
        from django.utils import timezone
        ahora = timezone.now()
        if not self.activo:
            return False, "Este cupom não está mais ativo."
        if ahora < self.fecha_inicio or ahora > self.fecha_fin:
            return False, "Este cupom expirou ou ainda não está disponível."
        if self.usos_actuales >= self.usos_maximos:
            return False, "Este cupom atingiu o limite de usos."
        if total_carrito < self.compra_minima:
            return False, f"Valor mínimo de R$ {self.compra_minima} para usar este cupom."
        return True, ""

    def calcular_descuento(self, total_carrito):
        if self.tipo == 'porcentaje':
            return total_carrito * (self.valor / 100)
        return min(self.valor, total_carrito)
