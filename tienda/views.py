from django.shortcuts import render, get_object_or_404
from .models import Producto

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
    return render(request, 'tienda/shopping-cart.html')

def checkout(request):
    return render(request, 'tienda/checkout.html')

def order_confirmed(request):
    return render(request, 'tienda/order-confirmed.html')