# 📚 Sistema de Gestión para Librerías

Aplicación web completa para la administración de librerías físicas o digitales. Permite gestionar el catálogo de libros, registrar ventas, visualizar estadísticas y exportar datos, todo con una interfaz moderna y adaptable (tema oscuro/claro).

![Estado](https://img.shields.io/badge/estable-v1.0-green)
![Licencia](https://img.shields.io/badge/licencia-MIT-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)

---

## ✨ Características principales

- 📖 **Gestión de catálogo**: CRUD completo de libros (título, autor, ISBN, ejemplares, stock, versión digital, estado de imprenta).
- 💰 **Registro de ventas**: Asociación de ventas a clientes, libros, eventos y sucursales. Cálculo automático del total.
- 📊 **Dashboard y estadísticas**: Visualización de ingresos, títulos más vendidos, clientes frecuentes, ventas por evento y mucho más.
- 🌓 **Tema oscuro/claro**: Interfaz adaptable con persistencia de preferencia.
- 🔐 **Autenticación**: Sistema de login con cambio de contraseña y sesión recordable.
- 🖼️ **Personalización**: Carga de logo y nombre de la librería.
- 📁 **Exportación a CSV**: Descarga de catálogo e historial de ventas.
- 🗃️ **Base de datos local**: Utiliza SQLite, sin necesidad de servidor externo.
- 🚀 **Listo para usar**: Asistente de configuración inicial en primera ejecución.

---

## 🖥️ Tecnologías utilizadas

| Capa        | Tecnologías                         |
|-------------|--------------------------------------|
| Frontend    | HTML5, CSS3, JavaScript (vanilla)   |
| Backend     | Python 3 (HTTP server nativo)       |
| Base de datos | SQLite3                           |
| Estilos     | CSS Grid, Flexbox, variables CSS    |
| Iconos      | SVG inline                          |

---

## 📦 Estructura del proyecto
proyecto/
├── app.html # Interfaz completa (frontend)

├── main.py # Servidor HTTP y lógica backend

├── data/ # Base de datos SQLite (catalogo.db, ventas.db, app.db)

├── assets/ # Logos e imágenes subidas por el usuario

└── README.md # Este archivo


---

## 🚀 Instalación y ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/sistema-libreria.git
cd sistema-libreria

2. Ejecutar el servidor
python main.py

⚠️ Requisito: Python 3.7 o superior (sin dependencias externas).

3. Acceder a la aplicación
El servidor abrirá automáticamente tu navegador en:
http://127.0.0.1:8765

4. Primera ejecución
Se mostrará un asistente de configuración para:

Nombre de la librería

Logo (opcional)

Usuario y contraseña de administrador

Selección de tema visual

Una vez completado, se iniciará la sesión automáticamente.

🧑‍💻 Uso del sistema
🔐 Acceso
Ingresá con el usuario y contraseña creados en el setup.

Podés marcar "Recordar sesión" para evitar volver a escribir credenciales.

📖 Catálogo
Agregar, editar o eliminar libros.

Filtrar por búsqueda (título, autor, ISBN), disponibilidad digital o stock.

Ordenar columnas haciendo clic en los encabezados de la tabla.

💸 Ventas
Registrar nuevas ventas asociando un libro existente.

Visualizar resumen de ingresos, unidades vendidas y ticket promedio.

Filtrar por fecha (mes) y por cliente/libro/evento.

📊 Estadísticas
Ranking de ingresos por libro y por cliente.

Gráficos de barras dinámicos.

Detalle por título (transacciones, unidades, ingresos).

⚙️ Configuración
Cambiar nombre y logo de la librería.

Alternar entre tema oscuro/claro.

Cambiar contraseña del usuario.

Exportar todos los datos a CSV.

🗄️ Bases de datos
El sistema genera automáticamente tres archivos SQLite en la carpeta data/:

Archivo	Contenido
app.db	Usuarios y configuración general (nombre, logo, tema, setup_done)
catalogo.db	Tabla libros con todos los títulos
ventas.db	Tabla ventas con el historial completo
✅ No requiere instalación de MySQL, PostgreSQL ni ningún otro motor.

🛠️ API interna (endpoints)
El frontend se comunica con el backend mediante una API REST simple:

Método	Endpoint	Descripción
GET	/api/status	Estado del sistema y configuración
GET	/api/libros	Obtener todos los libros
GET	/api/ventas	Obtener todas las ventas
POST	/api/setup	Configuración inicial
POST	/api/login	Autenticación de usuario
POST	/api/libros	Agregar libro
PUT	/api/libros/{id}	Editar libro
DELETE	/api/libros/{id}	Eliminar libro
POST	/api/ventas	Registrar venta
DELETE	/api/ventas/{id}	Eliminar venta
POST	/api/config	Actualizar nombre/logo/tema
POST	/api/change-password	Cambiar contraseña
🧪 Personalización y desarrollo
Cambiar puerto del servidor
Editá las constantes en main.py:
HOST, PORT = "127.0.0.1", 8765

Modificar estilos
Todos los estilos se encuentran en el <style> dentro de app.html. Usa variables CSS para adaptar colores, fuentes o espaciados.

Agregar campos a libros o ventas
Deberás modificar:

El HTML de los modales.

Las funciones JavaScript de agregar/editar.

Las consultas SQL en main.py.

La estructura de las tablas (el sistema migrará automáticamente en la próxima ejecución).

🧰 Posibles problemas y soluciones
Problema	Solución
El puerto 8765 ya está en uso	Cambiar PORT en main.py a otro número (ej. 9000).
El logo no se guarda	Verificar que la carpeta assets/ tenga permisos de escritura.
Error de CORS al hacer fetch	El servidor ya incluye los headers necesarios.
Las tablas no se crean	Asegurar que la carpeta data/ existe y es escribible.
📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Podés usarlo, modificarlo y distribuirlo libremente.

👥 Autor
Desarrollado como solución integral para la gestión de librerías.
¿Preguntas o sugerencias? ¡Abrí un issue o enviá un pull request!
