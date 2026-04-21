# Sistema de Gestion para Librerias

Sistema de gestion de catalogo y ventas para librerias, desarrollado en Python con interfaz web local.

## Caracteristicas

- Catalogo de libros — alta, edicion, eliminacion, busqueda y filtros
- Registro de ventas — con calculo automatico de totales
- Dashboard — metricas e ingresos en tiempo real
- Estadisticas — ranking por titulo, cliente y evento
- Exportacion CSV
- Modo oscuro / claro
- Configuracion por libreria — nombre, logo y credenciales propias
- Icono en bandeja del sistema — cierre limpio del servidor
- Sin dependencias externas — funciona completamente offline

## Instalacion (usuarios finales)

Descarga el instalador desde la seccion **Releases** y ejecutalo.
No necesitas instalar Python ni ningun otro programa.

## Desarrollo local

### Requisitos
- Python 3.10 o superior

### Instalar dependencias
```
pip install pystray pillow
```

### Ejecutar
```
python main.py
```
Se abre automaticamente en http://127.0.0.1:8765

## Compilar el instalador

### Requisitos
- Python 3.10+ con pip
- Inno Setup 6 (https://jrsoftware.org/isinfo.php)

### Pasos
1. Ejecutar build.bat — genera dist\SistemaLibreria.exe
2. Abrir instalador\setup.iss con Inno Setup y presionar F9
3. El instalador queda en output_instalador\

## Estructura del proyecto

```
main.py                  Servidor HTTP y logica de negocio
app.html                 Interfaz web completa
build.bat                Script de compilacion automatica
SistemaLibreria.spec     Configuracion de PyInstaller
data/
  catalogo.db            Base de datos de libros
  ventas.db              Base de datos de ventas
assets/                  Logos (generados en uso)
instalador/
  setup.iss              Script del instalador Inno Setup
```

## Tecnologias

- Backend: Python 3, http.server, sqlite3
- Frontend: HTML5, CSS3, JavaScript vanilla
- Base de datos: SQLite3
- Empaquetado: PyInstaller
- Instalador: Inno Setup 6
- System tray: pystray + Pillow

## Licencia

MIT License
