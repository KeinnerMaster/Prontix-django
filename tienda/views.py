from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Categoria, Pedido, ItemPedido
from .cart import Cart
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    productos_destacados = Producto.objects.filter(destacado=True, activo=True)[:4]
    context = {
        'productos': productos_destacados
    }
    return render(request, 'tienda/index.html', context)

def producto_detalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug, activo=True)
    relacionados = Producto.objects.filter(categoria=producto.categoria, activo=True).exclude(id=producto.id)[:4]
    context = {
        'producto': producto,
        'relacionados': relacionados
    }
    return render(request, 'tienda/product-detail.html', context)

def about(request):
    return render(request, 'tienda/about.html')

def contact(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        cuerpo = f"Nome: {nombre}\nEmail: {email}\nAssunto: {asunto}\n\nMensagem:\n{mensaje}"

        try:
            send_mail(
                subject=f'[HOCCE Contato] {asunto}',
                message=cuerpo,
                from_email=None,
                recipient_list=[getattr(settings, 'CONTACT_EMAIL_DESTINO', 'hoccebr@gmail.com')],
                fail_silently=False,
            )
            messages.success(request, 'Mensagem enviada com sucesso! Responderemos em breve.')
        except Exception as e:
            print(f"ERROR EMAIL: {e}")
            messages.error(request, 'Erro ao enviar a mensagem. Tente novamente mais tarde.')

        return redirect('contact')

    return render(request, 'tienda/contact.html')

def faq(request):
    return render(request, 'tienda/faq.html')

def privacy(request):
    return render(request, 'tienda/privacy-policy.html')

def cart(request):
    carrito = Cart(request)
    context = {
        'carrito': carrito,
    }
    return render(request, 'tienda/shopping-cart.html', context)


def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = Cart(request)
    carrito.agregar(producto, cantidad)
    messages.success(request, f'{producto.nombre} añadido al carrito.')
    return redirect('cart')


def update_cart_item(request, producto_id):
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = Cart(request)
    carrito.actualizar_cantidad(producto_id, cantidad)
    return redirect('cart')


def remove_from_cart(request, producto_id):
    carrito = Cart(request)
    carrito.eliminar(producto_id)
    messages.info(request, 'Producto eliminado del carrito.')
    return redirect('cart')

def checkout(request):
    return render(request, 'tienda/checkout.html')

def order_confirmed(request):
    return render(request, 'tienda/order-confirmed.html')

def catalogo(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_activa': categoria_slug,
    }
    return render(request, 'tienda/catalogo.html', context)

def checkout(request):
    carrito = Cart(request)

    if len(carrito) == 0:
        return redirect('cart')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        notas = request.POST.get('notas', '')

        pedido = Pedido.objects.create(
            nombre_cliente=nombre,
            email_cliente=email,
            telefono_cliente=telefono,
            direccion=direccion,
            ciudad=ciudad,
            notas=notas,
            total=carrito.total(),
        )

        for item in carrito:
            ItemPedido.objects.create(
                pedido=pedido,
                producto=item['producto'],
                nombre_producto=item['producto'].nombre,
                precio_unitario=item['precio_unitario'],
                cantidad=item['cantidad'],
            )
            # Descontar del stock
            producto = item['producto']
            producto.stock = max(0, producto.stock - item['cantidad'])
            producto.save()

        carrito.vaciar()
        request.session['ultimo_pedido_id'] = pedido.id

        return redirect('order_confirmed')

    context = {'carrito': carrito}
    return render(request, 'tienda/checkout.html', context)


def order_confirmed(request):
    pedido_id = request.session.get('ultimo_pedido_id')
    pedido = None
    if pedido_id:
        pedido = Pedido.objects.filter(id=pedido_id).first()
    context = {'pedido': pedido}
    return render(request, 'tienda/order-confirmed.html', context)
