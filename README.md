# OCR Captcha Resolver - Entregable

Esta carpeta contiene la versión entregable del proyecto con el script Python y el ejecutable listos para usar.

## Estructura de la carpeta `entregable`

- `README.md` - Documentación de uso para esta carpeta.
- `033_ATM_CaptchaResolver.py` - Script principal que carga el modelo ONNX y procesa una imagen de captcha.
- `033_ATM_CaptchaResolver.exe` - Ejecutable empaquetado del mismo script.
- `model\captcha_model.onnx` - Archivo principal del modelo entrenado.
- `model\captcha_model.onnx.data` - Archivo de datos externos para el modelo.
- `model\vocab.json` - Vocabulario usado para decodificar la salida del modelo.

## Requisitos

Para ejecutar este entregable en Windows necesitas:

1. Python 3.11 o superior instalado.
2. pip y uv instalado de manera global.

## Instalación y configuración

### 1. Instalar uv (solo la primera vez)

Abre PowerShell o CMD e instala `virtualenv` de forma global:

```powershell
pip install uv
```

Si `pip` no se reconoce, asegúrate de que Python está instalado y agregado al PATH.

### 2. Abrir una terminal en la carpeta del proyecto
Navega a la carpeta donde extrajiste el proyecto:

```powershell
cd "C:\ruta\hacia\proyecto"
```

### 3. Activar un entorno virtual con virtualenv

Activar el entorno virtual:

```powershell
.\venv\Scripts\Activate
```

### 4.Iniicializar proyecto



## Uso básico

### Ejecutar el script Python

```powershell
python .\src\033_ATM_CaptchaResolver.py "C:\ruta\hacia\imagen.jpg"
```

Reemplaza `C:\ruta\hacia\imagen.jpg` con la ruta completa o relativa a tu imagen de captcha. Ejemplos:
- Ruta completa: `C:\Users\Usuario\Pictures\captcha.jpg`
- Ruta relativa (imagen en carpeta padre): `..\captchas\ZJPF.jpg`
- Ruta relativa (imagen en la misma carpeta): `.\ZJPF.jpg`

### Ejecutar el .exe empaquetado

Desde la carpeta `entregable`, ejecuta:

```powershell
.\033_ATM_CaptchaResolver.exe "C:\ruta\hacia\imagen.jpg"
```

Reemplaza `C:\ruta\hacia\imagen.jpg` con la ruta a tu imagen, tal como en el ejemplo anterior.

## Archivos que debe encontrar el script

El script busca los archivos junto a él dentro de la carpeta `entregable`:

- `model\captcha_model.onnx`
- `model\captcha_model.onnx.data`
- `model\vocab.json`

Si ejecutas el script desde un ejecutable empaquetado, PyInstaller también cargará estos recursos desde su carpeta temporal.

## Cómo funciona el script

1. Carga el modelo ONNX desde `model\captcha_model.onnx`.
2. Carga el vocabulario desde `model\vocab.json`.
3. Preprocesa la imagen:
   - lee la imagen con OpenCV
   - aplica máscara en HSV
   - limpia ruido con inpainting
   - convierte a escala de grises
   - redimensiona a `128x48`
   - normaliza valores a rango `0-1`
4. Ejecuta la inferencia ONNX.
5. Decodifica la salida y devuelve el texto en mayúsculas.

## Solución de problemas comunes

- `ERROR: No se pudo leer la imagen`: revisa la ruta y el nombre del archivo.
- `ERROR: Modelo no encontrado`: verifica que `model\captcha_model.onnx` exista dentro de la carpeta `entregable`.
- `ERROR: Vocabulario no encontrado`: verifica que `model\vocab.json` exista dentro de la carpeta `entregable`.
- `python no se reconoce`: Python no está en PATH. Reinstala Python y marca `Add Python to PATH`.

## Nota

Este `README` está hecho específicamente para la carpeta `entregable`. El script busca los archivos del modelo junto a él, así que siempre ejecuta desde dentro de esta carpeta o usa rutas completas hacia el script.
