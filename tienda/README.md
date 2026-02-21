
### 🌐 **Páginas Públicas (Carpeta CLIENTE)**
- `index.html` - Página de inicio
- `about.html` - Sobre nosotros
- `contact.html` - Contacto
- `faq.html` - Preguntas frecuentes
- `privacy-policy.html` - Política de privacidad
- `product-detail.html` - Detalle de producto
- `shopping-cart.html` - Carrito de compras
- `checkout.html` - Proceso de pago
- `order-confirmed.html` - Confirmación de pedido

### 🔧 **Panel de Administración (Carpeta ADMIN)**
- `admin-dashboard.html` - Dashboard principal
- `admin-products.html` - Gestión de productos
- `admin-orders.html` - Gestión de pedidos
- `admin-customers.html` - Gestión de clientes
- `admin-analytics.html` - Analíticas y reportes
- `admin-coupons.html` - Gestión de cupones
- `admin-settings.html` - Configuración general
- `admin-shipping.html` - Configuración de envíos

## 🚀 **Instrucciones para subir a InfinityFree**

### 1. Prepara los archivos
- Asegúrate de tener la carpeta `greenery-web` completa en tu ordenador
- Verifica que contiene las subcarpetas `CLIENTE` y `ADMIN` con todos sus archivos

### 2. Conéctate a tu hosting
- Abre **FileZilla** (o cualquier cliente FTP)
- Conéctate usando los datos que te proporcionó InfinityFree:
  - **Servidor:** (ej: ftp.tudominio.com)
  - **Usuario:** (el que creaste)
  - **Contraseña:** (la que elegiste)
  - **Puerto:** 21

### 3. Sube los archivos
- En FileZilla, navega a la carpeta `htdocs` (lado derecho)
- **Arrastra toda la carpeta `greenery-web`** desde tu ordenador (lado izquierdo) a `htdocs`
- Espera a que se complete la subida

### 4. ¡Listo! Tu web está online
- **Tienda pública:** `http://tudominio.com/CLIENTE/`
- **Panel de admin:** `http://tudominio.com/ADMIN/admin-dashboard.html`

## 🔗 **Rutas importantes**
- Desde el ADMIN puedes ir a la tienda con el botón "View Store"
- Desde la tienda, los enlaces al ADMIN están en el panel de administración
- Todas las páginas están vinculadas entre sí

## ⚙️ **Personalización**
Puedes modificar:
- Los colores editando la variable `primary` en el `tailwind.config`
- Los textos y precios directamente en cada archivo HTML
- Las imágenes reemplazando las URLs de Google Cloud Storage

## 📝 **Notas**
- Es un sitio **estático** (solo HTML/CSS/JS)
- No requiere base de datos ni backend
- Las imágenes se cargan desde Google Cloud Storage
- Todo el estilo usa Tailwind CSS vía CDN

---

© 2024 Greenery Plant Store. Todos los derechos reservados.