from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    db.create_all()

    if not Usuario.query.filter_by(correo='admin@vetcare.com').first():
        admin = Usuario(
            nombre='Admin', apellido='VetCare',
            dni='00000000', telefono='0000000000',
            correo='admin@vetcare.com', rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
