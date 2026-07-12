from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('productos/', views.catalogo, name='catalogo'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('producto/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('carrito/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmado/', views.order_confirmed, name='order_confirmed'),
]
