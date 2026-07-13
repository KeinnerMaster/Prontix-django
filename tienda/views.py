from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Categoria
from .cart import Cart

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
