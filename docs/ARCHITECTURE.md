# Arquitectura del Sistema VetCare_Software

Este documento describe la estructura interna del proyecto, la organización de sus componentes principales y el flujo de datos bajo el patrón MVC (Modelo-Vista-Controlador).

---

## 📁 Estructura de Carpetas Real

El proyecto está estructurado de forma modular dentro del directorio principal `app/`, distribuyendo las responsabilidades de la siguiente manera:

```text
vetCare_Software/
│
├── app/
│   ├── __init__.py        # Inicializa Flask, SQLAlchemy, LoginManager y Blueprints
│   │
│   # Módulos y Modelos de Entidades (Capa del Modelo)
│   ├── usuario.py         # Modelo de Usuarios (Autenticación, Roles y Hash)
│   ├── mascota.py         # Modelo de Pacientes (Especie, Raza, Dueño)
│   ├── turno.py           # Modelo de Agenda de Turnos y Estados
│   ├── tienda.py          # Modelos de E-commerce (Producto, Carrito, Compra)
│   ├── historia_clinica.py# Modelos Médicos (Diagnóstico, Tratamiento, Medicamento)
│   │
│   ├── routes/            # Capa del Controlador (Lógica de negocio y Blueprints)
│   │   ├── turnos.py      # Rutas para gestión de citas
│   │   ├── usuarios.py    # Rutas para login, registro y perfiles
│   │   └── [otras rutas]  # Rutas de tienda, historias clínicas, etc.
│   │
│   ├── templates/         # Capa de la Vista (Interfaz de Usuario / Jinja2)
│   └── static/            # Archivos estáticos del Frontend (CSS, JS, Bootstrap)
│
├── requirements.txt       # Dependencias y librerías del proyecto
├── run.py                 # Punto de entrada principal para ejecutar la aplicación
└── docs/                  # Documentación técnica y funcional del proyecto
