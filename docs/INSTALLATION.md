Para que no reniegues, acá tenés el archivo **corregido por completo**. Copiá todo el bloque de acá abajo de un tirón, reemplazá lo que tenés en tu archivo local y metele ese `git commit` con total confianza:

```markdown
# Manual de Instalación y Ejecución

Este documento explica de forma detallada los pasos necesarios para clonar, configurar, instalar las dependencias y ejecutar el sistema **VetCare_Software** en un entorno de desarrollo local.

---

## 📋 Requisitos Previos

Antes de comenzar, asegurate de tener instalado en tu sistema lo siguiente:
- **Python 3.10 o superior** (Asegurate de marcar la opción "Add Python to PATH" durante la instalación en Windows).
- **Git** (Para la gestión y clonación del repositorio).
- Un navegador web moderno y actualizado (Chrome, Firefox, Edge, Safari).

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el repositorio
Abran una terminal en su máquina, posicionense en la carpeta donde deseen guardar el proyecto y ejecuten el comando para clonar:
```bash
git clone https://github.com/Pabb-J/vetCare_Software.git
cd vetCare_Software
```

### 2. Crear un Entorno Virtual (`venv`)
Es una buena práctica crear un entorno aislado para evitar conflictos entre las versiones de las librerías de Python.

* **En Windows (Command Prompt / PowerShell):**
```bash
python -m venv venv
```

* **En macOS / Linux:**
```bash
python3 -m venv venv
```

### 3. Activar el Entorno Virtual
Debés activar el entorno virtual cada vez que vayas a trabajar en el proyecto o a ejecutar el servidor.

* **En Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

* **En Windows (CMD / Símbolo del sistema):**
```bash
venv\Scripts\activate.bat
```

* **En macOS / Linux:**
```bash
source venv/bin/activate
```
*(Sabrás que está activo porque aparecerá `(venv)` al principio de la línea de comandos de tu terminal).*

### 4. Instalar las dependencias del sistema
Con el entorno virtual activo, ejecutá el siguiente comando para instalar todos los paquetes y extensiones requeridas por la aplicación (Flask, Flask-SQLAlchemy, Flask-Login, etc.):
```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuración Inicial y Base de Datos

El sistema utiliza **SQLite** por defecto para el entorno de desarrollo, lo que significa que la base de datos se creará automáticamente como un archivo local en la raíz del proyecto.

Si el script principal de tu aplicación no incluye la directiva automática `db.create_all()`, podés generar las tablas abriendo una terminal interactiva de Python y corriendo:

```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

---

## 💻 Ejecución del Servidor

Una vez completados los pasos anteriores, estás listo para levantar la aplicación. Asegurate de estar en la raíz de la carpeta `vetCare_Software` y con el entorno virtual activo:

```bash
python run.py
```
*(Nota: Si tu archivo principal de arranque tiene otro nombre, reemplazá `run.py` por el archivo correspondiente, por ejemplo: `flask run` o `python app.py`).*

Cuando la terminal indique que el servidor está corriendo, abrí tu navegador web e ingresá a la siguiente dirección URL:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)** o **[http://localhost:5000/](http://localhost:5000/)**

---

## 🛑 Cómo Detener el Servidor
Para apagar el servidor de Flask en cualquier momento, presioná la combinación de teclas **`Ctrl + C`** en la terminal. 

Para salir del entorno virtual de Python, simplemente ejecutá:
```bash
deactivate
