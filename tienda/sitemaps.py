from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Producto


class ProductoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Producto.objects.filter(activo=True)

    def location(self, obj):
        return reverse('producto_detalle', args=[obj.slug])


class PaginasEstaticasSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['index', 'catalogo', 'about', 'contact', 'faq', 'shipping_policy', 'privacy']

    def location(self, item):
        return reverse(item)
