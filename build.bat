@echo off
chcp 437 >nul
title Compilando...
color 0A

echo.
echo ============================================
echo  Sistema de Gestion para Librerias
echo  Script de compilacion
echo ============================================
echo.

echo [1/5] Verificando Python...
python --version
if errorlevel 1 (
    echo [ERROR] Python no encontrado.
    echo Instala Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH"
    pause
    exit /b 1
)
echo [OK] Python encontrado.
echo.

echo [2/5] Instalando PyInstaller...
python -m pip install pyinstaller --upgrade --quiet
if errorlevel 1 (
    echo [ERROR] No se pudo instalar PyInstaller.
    pause & exit /b 1
)
echo [OK] PyInstaller listo.
echo.

echo [3/5] Instalando pystray y Pillow (icono de bandeja)...
python -m pip install pystray pillow --upgrade --quiet
if errorlevel 1 (
    echo [ERROR] No se pudo instalar pystray o Pillow.
    pause & exit /b 1
)
echo [OK] pystray y Pillow listos.
echo.

echo [4/5] Compilando el ejecutable...
echo Esto puede tardar entre 2 y 4 minutos, por favor espera.
echo.

if not exist "assets" mkdir assets
if not exist "data" mkdir data
if not exist "output_instalador" mkdir output_instalador

python -m PyInstaller SistemaLibreria.spec --clean --noconfirm
if errorlevel 1 (
    echo.
    echo [ERROR] La compilacion fallo.
    echo Revisa los mensajes de error arriba.
    pause & exit /b 1
)

echo.
echo [5/5] Verificando resultado...
if exist "dist\SistemaLibreria.exe" (
    echo.
    echo ============================================
    echo  COMPILACION EXITOSA
    echo.
    echo  Ejecutable: dist\SistemaLibreria.exe
    echo.
    echo  NOVEDAD: el programa ahora muestra un
    echo  icono en la bandeja del sistema.
    echo  Para cerrarlo: clic derecho en el icono
    echo  y elegir "Cerrar el programa".
    echo.
    echo  SIGUIENTE PASO:
    echo  Prueba el .exe y luego abre Inno Setup
    echo  con: instalador\setup.iss
    echo ============================================
) else (
    echo [ERROR] No se encontro dist\SistemaLibreria.exe
    pause & exit /b 1
)

echo.
pause
