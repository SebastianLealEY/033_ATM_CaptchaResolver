# 033 — ATM CaptchaResolver

Herramienta para resolver automáticamente los CAPTCHAs del sistema **SIGA**. Utiliza visión por computadora (OpenCV) e inferencia con modelos ONNX para identificar y resolver los desafíos visuales sin intervención manual.

---

## Requisitos previos

| Herramienta | Versión requerida | Descarga |
|---|---|---|
| Python | **3.14.2** (exacta) | [python.org](https://www.python.org/downloads/) |
| uv *(gestor de paquetes)* | Última versión | Ver instrucciones abajo |
| Git | Cualquier versión reciente | [git-scm.com](https://git-scm.com/) |

> ⚠️ El proyecto requiere **exactamente Python 3.14.2**. Versiones distintas pueden causar incompatibilidades con las dependencias.

---

## Instalación paso a paso

### 1. Instalar `uv`

`uv` es el gestor de entornos y paquetes que usa este proyecto.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verifica la instalación:
```bash
uv --version
```

---

### 2. Clonar el repositorio

```bash
git clone https://github.com/SebastianLealEY/033_ATM_CaptchaResolver.git
cd 033_ATM_CaptchaResolver
```

---

### 3. Instalar Python 3.14.2 con `uv`

```bash
uv python install 3.14.2
```

---

### 4. Crear el entorno virtual e instalar dependencias

```bash
uv sync
```

Este comando lee el archivo `pyproject.toml` e instala automáticamente:
- `numpy 2.4.4`
- `onnxruntime 1.25.1`
- `opencv-python 4.13.0.92`

---

### 5. Ejecutar el script

El script recibe como argumento la **ruta a la imagen** del CAPTCHA que se desea resolver:

```bash
uv run main.py <ruta_de_imagen>
```

**Ejemplos:**

```bash
# Windows
uv run main.py C:\captchas\imagen.png

# macOS / Linux
uv run main.py /home/usuario/captchas/imagen.png

# Ruta relativa
uv run main.py ./captcha.png
```

---

## Generar un ejecutable `.exe`

El proyecto incluye **PyInstaller** como dependencia de desarrollo para compilar el script en un ejecutable independiente (solo Windows).

### Paso 1: Instalar dependencias de desarrollo

```bash
uv sync --group dev
```

### Paso 2: Generar el `.exe`

El ejecutable debe incluir los archivos del modelo ONNX que se encuentran dentro de la carpeta `model/`. Se usa la flag `--add-data` para empaquetar cada archivo:

**Windows (PowerShell):**
```powershell
uv run pyinstaller --onefile `
  --add-data "model/*.onnx;model" `
  --add-data "model/*.onnx.data;model" `
  --add-data "model/vocab.json;model" `
  main.py
```

**macOS / Linux:**
```bash
uv run pyinstaller --onefile \
  --add-data "model/*.onnx:model" \
  --add-data "model/*.onnx.data:model" \
  --add-data "model/vocab.json:model" \
  main.py
```

> ℹ️ La diferencia entre Windows y macOS/Linux está en el separador de rutas dentro de `--add-data`: Windows usa `;`, los demás usan `:`.

El archivo ejecutable se generará en la carpeta `dist/`:

```
dist/
└── main.exe
```

Y se usa igual que el script, pasando la ruta de la imagen como argumento:

```bash
dist\main.exe C:\captchas\imagen.png
```

### Opciones útiles de PyInstaller

| Opción | Descripción |
|---|---|
| `--onefile` | Empaqueta todo en un único `.exe` |
| `--add-data "src;dest"` | Incluye archivos adicionales (modelos, configs, etc.) |
| `--noconsole` | Oculta la ventana de consola (útil si hay interfaz gráfica) |
| `--name MiApp` | Cambia el nombre del ejecutable generado |
| `--icon icono.ico` | Asigna un ícono al ejecutable |

**Ejemplo con nombre personalizado (Windows):**
```powershell
uv run pyinstaller --onefile --name CaptchaResolver `
  --add-data "model/*.onnx;model" `
  --add-data "model/*.onnx.data;model" `
  --add-data "model/vocab.json;model" `
  main.py
```

---

## Estructura del proyecto

```
033_ATM_CaptchaResolver/
├── src/                  # Módulos internos del proyecto
├── model/                # Archivos del modelo ONNX (requeridos)
│   ├── *.onnx            # Modelo de inferencia
│   ├── *.onnx.data       # Pesos del modelo
│   └── vocab.json        # Vocabulario para decodificación
├── main.py               # Punto de entrada principal
├── pyproject.toml        # Configuración del proyecto y dependencias
├── uv.lock               # Versiones exactas bloqueadas de dependencias
├── .python-version       # Versión de Python requerida (3.14.2)
└── .gitignore
```

---

## Solución de problemas comunes

**`uv` no se reconoce como comando:**
Cierra y vuelve a abrir la terminal después de instalar `uv`, o agrega su ruta al `PATH` manualmente.

**Error de versión de Python:**
Asegúrate de usar exactamente Python 3.14.2. Ejecuta `uv python list` para ver las versiones instaladas.

**El `.exe` no ejecuta en otra PC:**
El ejecutable generado con `--onefile` es autocontenido, pero solo funciona en el mismo sistema operativo donde fue compilado (Windows → Windows).

**Antivirus bloquea el `.exe`:**
Los ejecutables generados con PyInstaller pueden ser marcados como falsos positivos. Agrega una excepción en tu antivirus o compila en un entorno de confianza.
