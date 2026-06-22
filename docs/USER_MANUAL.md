Manual de Usuario - VetCare_Software

Este manual práctico está diseñado para guiar tanto a clientes (dueños de mascotas) como al personal médico (veterinarios) y administradores en el uso cotidiano de la aplicación VetCare_Software.

1. Introducción

VetCare_Software es una plataforma web veterinaria integral orientada a simplificar la administración clínica y comercial. El sistema permite:

Gestionar el registro de pacientes (mascotas) y dueños de forma centralizada.

Agendar, controlar y cancelar turnos médicos interactivos.

Administrar historias clínicas, diagnósticos, medicamentos y tratamientos.

Acceder a una tienda virtual integrada con carrito de compras y control de stock.

2. Requisitos Previos

Para utilizar la aplicación sin inconvenientes, solo se necesita:

Un dispositivo con navegador web moderno instalado (Google Chrome, Mozilla Firefox, Microsoft Edge o Safari).

Conexión activa a la red local o a internet (según dónde esté alojado el servidor).

Una cuenta activa con su correspondiente correo electrónico y contraseña.

3. Primeros Pasos y Acceso al Sistema

3.1. Inicio de Sesión (Login)

Abra el navegador web y acceda a la URL de la clínica (por defecto en desarrollo: http://localhost:5000).

En la pantalla de bienvenida, ingrese su correo electrónico y contraseña.

Haga clic en el botón "Iniciar Sesión".

3.2. Panel Principal (Dashboard)

Una vez autenticado, el sistema lo redirigirá a una interfaz personalizada basada en su rol de usuario asignado (Cliente, Veterinario o Administrador).

4. Funciones según el Rol de Usuario

4.1. Módulo para Clientes (Dueños de Mascotas)

Como cliente, usted tiene el control de sus datos, sus mascotas y sus compras:

A. Mis Mascotas

Visualización: Acceda a la sección "Mis Mascotas" para ver el listado de todos sus animales registrados.

Registrar Mascota: Presione el botón "Registrar Nueva Mascota". Complete el formulario con:

Nombre completo de la mascota.

Especie (ej: Perro, Gato, Ave).

Raza (ej: Labrador, Mestizo, Siamés).

Edad (en años).

Peso actual (en kg).

Guardar: Confirme la operación para vincular inmediatamente la mascota a su perfil.

B. Reservar un Turno

Diríjase a la sección "Solicitar Turno".

Seleccione cuál de sus mascotas registradas asistirá a la consulta.

Elija el veterinario de preferencia.

Seleccione la fecha y el horario disponible de la agenda.

Indique el motivo o tipo de consulta (ej: "Vacunación", "Control general").

Confirme la reserva. El turno cambiará automáticamente su estado a "ocupado".

C. Tienda Virtual (E-commerce)

Navegue por el catálogo de productos disponibles en la "Tienda".

Utilice el botón "Agregar al Carrito" para seleccionar los alimentos, accesorios o medicamentos que desee comprar.

Desde el panel del Carrito, verifique las cantidades y el subtotal calculado.

Presione "Confirmar Compra" para liquidar el pedido. El sistema actualizará el stock físico y registrará la orden en su historial de compras.

4.2. Módulo para Veterinarios (Personal Médico)

El equipo de salud veterinaria dispone de herramientas optimizadas para la atención clínica:

A. Agenda de Turnos Asignados

Consulte su panel diario para ver el listado de turnos bajo el estado "ocupado" que tienen su nombre asignado.

Podrá visualizar los datos de la mascota, el nombre del dueño, el horario de la cita y el tipo de consulta.

B. Apertura y Gestión de Historias Clínicas

Durante la consulta médica, el veterinario podrá abrir la ficha médica del paciente para redactar la consulta:

Emitir Diagnóstico: Registre una descripción técnica y observaciones sobre el estado de salud detectado en la mascota.

Asignar Tratamiento: Si la patología lo requiere, redacte un tratamiento indicando la descripción, la duración estimada (ej: "7 días") e indicaciones especiales de cuidado.

Prescribir Medicamentos: Ingrese el nombre del fármaco, la dosis precisa (ej: "2.5 mg" o "1 comprimido"), la frecuencia de toma (ej: "cada 12 horas") y la duración recomendada.

Guardar Ficha: Guarde los datos para que queden anexados permanentemente a la historia clínica histórica de la mascota.

4.3. Módulo para Administradores

El usuario con rol de Administrador tiene acceso total a los parámetros globales del sistema:

Gestión de Usuarios: Creación, edición y suspensión de cuentas de clientes y veterinarios (control de estado activo/inactivo).

Control de Inventario de Tienda: Carga de nuevos productos con sus respectivas imágenes, precios, descripción, categoría y unidades en stock.

Auditoría de Turnos: Visualización del cronograma general de atención clínica para evitar superposiciones u optimizar las agendas de los veterinarios.

5. Capturas de Pantalla (Ayuda Visual)

En esta sección se ilustra la navegación básica mediante maquetas del diseño:

Pantalla de Inicio y Log-in

``

Vista del Historial Clínico (Panel Veterinario)

``

Catálogo de Compra de la Tienda (Panel Cliente)

``

6. Resolución de Problemas Comunes (FAQ)

❓ No puedo iniciar sesión en la plataforma

Solución: Verifique que el correo electrónico ingresado no contenga espacios innecesarios y que coincida exactamente con el registrado. Recuerde que el sistema distingue entre mayúsculas y minúsculas en las contraseñas. Si el problema persiste, consulte al administrador para comprobar si su usuario está marcado como "activo".

❓ No puedo visualizar el botón para recetar medicamentos

Solución: Esta opción está restringida únicamente para usuarios autenticados con el rol de Veterinario. Si es cliente o administrador, no tendrá acceso de escritura sobre los registros médicos.

❓ Intenté reservar un turno pero el horario no aparece

Solución: Un horario desaparece automáticamente de la grilla de selección cuando ya ha sido reservado por otro cliente (cambiando su estado a "ocupado") o cuando el veterinario seleccionado no se encuentra disponible en esa franja horaria. Intente seleccionando otro profesional u otro horario disponible.

7. Soporte Técnico

Ante cualquier inconveniente de funcionamiento del sistema, caída del servidor local, o solicitudes de creación de nuevas cuentas de personal, póngase en contacto con el administrador técnico de la clínica a través de la oficina de soporte de VetCare Software.
