"""
Crea un usuario directamente en la base de datos.

Se usa principalmente para crear cuentas de administrador, ya que el
formulario público de registro (/registro) ya no permite elegir ese
rol (solo "dueno" o "veterinario").

Uso:
    python crear_usuario.py
"""
import sys
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()


def main():
    print("=== Crear nuevo usuario ===")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    dni = input("DNI: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()
    password = input("Contraseña: ").strip()

    rol = ""
    while rol not in ("dueno", "veterinario", "admin"):
        rol = input("Rol (dueno / veterinario / admin): ").strip().lower()

    with app.app_context():
        if Usuario.query.filter_by(correo=correo).first():
            print(f"Ya existe un usuario con el correo {correo}.")
            sys.exit(1)
        if Usuario.query.filter_by(dni=dni).first():
            print(f"Ya existe un usuario con el DNI {dni}.")
            sys.exit(1)

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono,
            correo=correo,
            rol=rol,
        )
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()
        print(f"\nUsuario '{correo}' creado correctamente con rol '{rol}'.")


if __name__ == "__main__":
    main()
