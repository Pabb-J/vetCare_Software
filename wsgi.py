from app import create_app, db
from app.models.usuario import Usuario
import logging
import sys

# Configure logging to output to stdout for Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = create_app()

with app.app_context():
    try:
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully")
        
        logger.info("Checking for admin user...")
        if not Usuario.query.filter_by(correo='admin@vetcare.com').first():
            logger.info("Creating admin user...")
            admin = Usuario(
                nombre='Admin', apellido='VetCare',
                dni='00000000', telefono='0000000000',
                correo='admin@vetcare.com', rol='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise
