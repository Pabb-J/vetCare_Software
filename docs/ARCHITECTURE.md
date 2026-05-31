# Arquitectura del Sistema VetCare_Software

Este documento describe la estructura interna del proyecto y cómo se organizan sus componentes principales.

---

## Estructura de carpetas

vetCare_Software/
│
├── app/
│   ├── init.py        # Inicializa la aplicación Flask y registra blueprints
│   ├── models/            # Modelos de datos (ej: Turno, Mascota, Usuario)
│   ├── routes/            # Rutas y controladores (ej: turnos.py, usuarios.py)
│   ├── templates/         # Plantillas HTML (interfaz de usuario)
│   ├── static/            # Archivos estáticos (CSS, JS, imágenes)
│
├── requirements.txt       # Dependencias del proyecto
├── run.py                 # Punto de entrada para ejecutar la aplicación
└── docs/                  # Documentación del proyecto

## Codigo

---

## Componentes principales

- **Flask App (`app/__init__.py`)**  
  Configura la aplicación, inicializa extensiones y registra los módulos (blueprints).

- **Modelos (`app/models/`)**  
  Contienen las clases que representan las entidades del sistema (ejemplo: `Turno`, `Mascota`, `Usuario`).  
  Se utilizan con SQLite para persistencia de datos.

- **Rutas (`app/routes/`)**  
  Definen la lógica de negocio y las URL disponibles.  
  Ejemplo: `turnos.py` maneja creación, listado y cancelación de turnos.

- **Templates (`app/templates/`)**  
  Archivos HTML que renderizan la interfaz de usuario.  
  Usan Jinja2 para mostrar datos dinámicos.

- **Static (`app/static/`)**  
  Archivos CSS, JavaScript y recursos gráficos que complementan la interfaz.

---

## Flujo de ejecución

1. El usuario accede a la aplicación vía navegador.  
2. Flask recibe la petición y la redirige al blueprint correspondiente.  
3. El blueprint consulta o modifica datos en los modelos.  
4. Se renderiza una plantilla HTML con los resultados.  
5. El usuario visualiza la respuesta en el navegador.

---

## Notas
- La modularidad con **blueprints** permite escalar el sistema agregando nuevos módulos (ej: facturación, reportes).  
- La carpeta `docs/` centraliza toda la documentación técnica y funcional.

