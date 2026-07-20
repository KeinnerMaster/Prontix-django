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

    def save_model(self, request, obj, form, change):
        estado_anterior = None
        if change and 'estado' in form.changed_data:
            estado_anterior = Pedido.objects.get(pk=obj.pk).estado

        super().save_model(request, obj, form, change)

        if estado_anterior is not None and estado_anterior != obj.estado:
            self._notificar_cliente(obj)

    def save_formset(self, request, form, formset, change):
        """Detecta cambios de estado hechos desde la edición masiva en la lista (list_editable)."""
        super().save_formset(request, form, formset, change)

    def _notificar_cliente(self, pedido):
        import resend
        from django.conf import settings

        mensajes_estado = {
            'pendiente': 'Seu pedido está pendente de pagamento.',
            'pagado': 'Recebemos o pagamento do seu pedido! Em breve ele será enviado.',
            'enviado': 'Seu pedido foi enviado! Em breve chegará até você.',
            'entregado': 'Seu pedido foi entregue. Obrigado por comprar na HOCCE!',
            'cancelado': 'Seu pedido foi cancelado.',
        }
        mensaje = mensajes_estado.get(pedido.estado, f'O status do seu pedido mudou para: {pedido.get_estado_display()}')

        try:
            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": "HOCCE <onboarding@resend.dev>",
                "to": [pedido.email_cliente],
                "subject": f'Atualização do seu pedido #{pedido.id} - HOCCE',
                "text": f"Olá {pedido.nombre_cliente},\n\n{mensaje}\n\nPedido #{pedido.id}\nTotal: R$ {pedido.total}\n\nObrigado por comprar com a gente!",
            })
        except Exception as e:
            print(f"ERROR notificando cliente: {e}")

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ('modo_mantenimiento',)

    def has_add_permission(self, request):
        # Evita que se creen múltiples registros de configuración
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
