from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.index, name='index'),                    # http://127.0.0.1:8000/
    path('about/', views.about, name='about'),              # http://127.0.0.1:8000/about/
    path('contact/', views.contact, name='contact'),        # http://127.0.0.1:8000/contact/
    path('faq/', views.faq, name='faq'),                    # http://127.0.0.1:8000/faq/
    path('privacy/', views.privacy, name='privacy'),        # http://127.0.0.1:8000/privacy/
    
    # Productos
    path('producto/<slug:slug>/', views.producto_detalle, name='producto_detalle'),  # URLs dinámicas
    
    # Carrito y checkout
    path('carrito/', views.cart, name='cart'),              # http://127.0.0.1:8000/carrito/
    path('checkout/', views.checkout, name='checkout'),     # http://127.0.0.1:8000/checkout/
    path('confirmado/', views.order_confirmed, name='order_confirmed'),  # http://127.0.0.1:8000/confirmado/
]