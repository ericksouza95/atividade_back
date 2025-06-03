from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import TaskList, Task
from .. import db

task_bp = Blueprint('task', __name__, url_prefix='/tasks')

# Listar todas as tarefas do usuário
@task_bp.route('/', methods=['GET'])
@login_required
def get_tasks():
    task_list = TaskList.query.filter_by(user_id=current_user.id).first()
    if not task_list:
        return jsonify([])
    tasks = Task.query.filter_by(list_id=task_list.id).all()
    return jsonify([
        {'id': t.id, 'description': t.description, 'done': t.done}
        for t in tasks
    ])

# Criar nova tarefa
@task_bp.route('/', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    description = data.get('description', '')
    if not description:
        return jsonify({'error': 'Descrição obrigatória'}), 400

    task_list = TaskList.query.filter_by(user_id=current_user.id).first()
    if not task_list:
        task_list = TaskList(name='Minha Lista', user_id=current_user.id)
        db.session.add(task_list)
        db.session.commit()

    task = Task(description=description, list_id=task_list.id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Tarefa criada'}), 201

#  Remover tarefa
@task_bp.route('/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarefa removida'})
