from datetime import datetime
from database import db

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String(20), default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self):
        """Méthode helper pour l'API JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at
        }