from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.catalogo, name='catalogo'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('politica-de-envio/', views.shipping_policy, name='shipping_policy'),
    path('producto/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/', views.cart, name='cart'),
    path('carrito/agregar/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('carrito/actualizar/<str:clave>/', views.update_cart_item, name='update_cart_item'),
    path('carrito/eliminar/<str:clave>/', views.remove_from_cart, name='remove_from_cart'),
    path('carrito/cupon/aplicar/', views.aplicar_cupon, name='aplicar_cupon'),
    path('carrito/cupon/quitar/', views.quitar_cupon, name='quitar_cupon'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmado/', views.order_confirmed, name='order_confirmed'),
    path('newsletter/suscribir/', views.suscribir_newsletter, name='suscribir_newsletter'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
