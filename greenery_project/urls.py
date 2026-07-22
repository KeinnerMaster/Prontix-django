from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from tienda.sitemaps import ProductoSitemap, PaginasEstaticasSitemap

sitemaps = {
    'productos': ProductoSitemap,
    'paginas': PaginasEstaticasSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('tienda.urls')),
]
