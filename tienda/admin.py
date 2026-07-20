from django.contrib import admin
from .models import Categoria, Producto, Variante, Pedido, ItemPedido, ImagenProducto, ConfiguracionSitio

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}


class VarianteInline(admin.TabularInline):
    """Permite agregar talla/color directamente dentro de la pantalla
    de edicion del producto, sin entrar a otra seccion."""
    model = Variante
    extra = 1


class ImagenProductoInline(admin.TabularInline):
    """Permite agregar varias fotos adicionales al producto."""
    model = ImagenProducto
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'destacado', 'activo']
    list_filter = ['categoria', 'destacado', 'activo']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ['precio', 'stock', 'destacado', 'activo']
    inlines = [VarianteInline, ImagenProductoInline]


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('producto', 'nombre_producto', 'variante_info', 'precio_unitario', 'cantidad', 'subtotal')
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'telefono_cliente', 'total', 'estado', 'creado_en')
    list_filter = ('estado', 'creado_en')
    list_editable = ('estado',)
    search_fields = ('nombre_cliente', 'email_cliente', 'telefono_cliente')
    readonly_fields = ('nombre_cliente', 'email_cliente', 'telefono_cliente', 'direccion', 'ciudad', 'notas', 'total', 'creado_en')
    inlines = [ItemPedidoInline]
