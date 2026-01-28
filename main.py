import os
from flask import Flask, jsonify, request
from controllers.todo_controller import ToDoController
from database import db
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # --- CONFIGURATION ---
    # Récupération sécurisée depuis le .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation de la DB
    db.init_app(app)

    # Création des tables
    with app.app_context():
        db.create_all()

    todo = ToDoController()

    # Vérification de l’état de l’API
    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok",
            "message": "L'API fonctionne"
        })

    # Liste toutes les tâches
    @app.get("/api/tasks")
    def list_tasks():
        tasks = todo.list_tasks()
        return jsonify({"tasks": [t.to_dict() for t in tasks]})

    # Crée une nouvelle tâche
    @app.post("/api/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = data.get("title", "")
        try:
            t = todo.add_task(title)
            return jsonify({"message": "Tâche créée avec succès", "task": t.to_dict()}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # Récupère une tâche par ID
    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id: int):
        try:
            t = todo.get_task(task_id)
            return jsonify(t.to_dict())
        except KeyError:
            return jsonify({"error": f"Tâche id={task_id} introuvable."}), 404

    # Met à jour une tâche (titre)
    @app.patch("/api/tasks/<int:task_id>")
    def update_task(task_id: int):
        data = request.get_json(silent=True) or {}
        try:
            updated = None
            if "title" in data:
                updated = todo.update_title(task_id, data["title"])
            return jsonify({"message": "Tâche mise à jour", "task": updated.to_dict()})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except KeyError:
            return jsonify({"error": f"Tâche id={task_id} introuvable."}), 404

    # Supprime une tâche par ID
    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id: int):
        try:
            title = todo.delete_task(task_id)
            return jsonify({"message": f"Tâche supprimée : {title}"}), 200
        except KeyError:
            return jsonify({"error": f"Tâche id={task_id} introuvable."}), 404

    return app

if __name__ == "__main__":
    app = create_app()
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode)