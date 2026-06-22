# Documentación del Proyecto VetCare_Software

Este directorio contiene la documentación técnica, arquitectónica y funcional del sistema **VetCare_Software**.

## Contenido
- [Manual de instalación](INSTALLATION.md)
- [Arquitectura del sistema](ARCHITECTURE.md)
- [Manual de usuario](USER_MANUAL.md)

---

### Objetivo del proyecto
**VetCare_Software** es una aplicación web robusta desarrollada en **Flask** para la gestión integral de clínicas veterinarias. El sistema no solo automatiza la asignación de turnos, sino que centraliza las historias clínicas médicas y ofrece una plataforma de e-commerce (tienda virtual) para los clientes.

### Tecnologías utilizadas
- **Backend:** Python 3.x & Flask (Framework principal)
- **Autenticación:** Flask-Login & Werkzeug (Seguridad y cifrado de contraseñas)
- **Base de Datos y ORM:** SQLite junto a **Flask-SQLAlchemy**
- **Frontend:** HTML5, CSS3, Bootstrap & Motor de plantillas **Jinja2**
- **Control de versiones:** Git / GitHub

### Alcance de los Módulos Implementados
* **Gestión de Usuarios:** Registro y autenticación con control de accesos por roles (*Administrador, Veterinario, Cliente*).
* **Control de Pacientes:** Administración de mascotas asociadas a sus respectivos dueños.
* **Historias Clínicas Dinámicas:** Registro de diagnósticos médicos con tratamientos detallados y prescripción de medicamentos (dosis y frecuencias).
* **Sistema de Turnos:** Agenda médica con control de estados (*disponible, ocupado, cancelado*).
* **Tienda Virtual (E-commerce):** Gestión de catálogo, stock de productos, carrito de compras persistente por usuario y cálculo automatizado de compras.

---

### Cómo usar esta documentación
Cada archivo dentro de este espacio está orientado a un público distinto para facilitar la evaluación y el despliegue del proyecto integrador:

- **[INSTALLATION.md](INSTALLATION.md)** → **Guía técnica** paso a paso para clonar, configurar el entorno virtual (`venv`), instalar dependencias (`requirements.txt`) y ejecutar el sistema en entorno local.
- **[ARCHITECTURE.md](ARCHITECTURE.md)** → **Explicación técnica** de la estructura interna del código, la relación de los modelos de la base de datos (ORMs) y el flujo de rutas del patrón MVC.
- **[USER_MANUAL.md](USER_MANUAL.md)** → **Guía práctica** orientada a los usuarios finales, detallando el flujo de trabajo según el rol asignado (cómo atiende un veterinario, cómo compra o saca turno un cliente).
