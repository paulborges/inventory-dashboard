from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """INITIALISING THE DATABASE WITH THE FLASK APP"""
    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()
        print("Database Tables created")