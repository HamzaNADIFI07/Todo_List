from models.task import Task
from database import db

class ToDoController:

    def list_tasks(self):
        """Retourne toutes les tâches depuis la DB"""
        return Task.query.order_by(Task.id).all()

    def add_task(self, title: str):
        """Ajoute une tâche en base"""
        title = (title or "").strip()
        if not title:
            raise ValueError("Le titre ne peut pas être vide.")
        
        new_task = Task(title=title)
        
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def get_task(self, task_id: int):
        """Récupère une tâche ou lève une erreur"""
        task = db.session.get(Task, task_id)
        
        if not task:
            raise KeyError("Tâche introuvable.")
        return task

    def update_title(self, task_id: int, title: str):
        """Met à jour le titre"""
        title = (title or "").strip()
        if not title:
            raise ValueError("Le titre ne peut pas être vide.")
        
        task = self.get_task(task_id)
        task.title = title
        db.session.commit()
        return task

    def delete_task(self, task_id: int):
        """Supprime la tâche"""
        task = self.get_task(task_id)
        title_copy = task.title
        
        db.session.delete(task)
        db.session.commit()
        return title_copy