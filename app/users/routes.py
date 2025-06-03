from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import TaskList, Task
from .. import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    task_list = TaskList.query.filter_by(user_id=current_user.id).first()

    # Cria lista padrão se não existir
    if not task_list:
        task_list = TaskList(name="Lista principal", user_id=current_user.id)
        db.session.add(task_list)
        db.session.commit()

    # Adiciona tarefa
    if request.method == 'POST':
        description = request.form['description']
        new_task = Task(description=description, list_id=task_list.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('user.dashboard'))

    # Exibe tarefas
    tasks = Task.query.filter_by(list_id=task_list.id).all()
    return render_template('dashboard.html', tasks=tasks)

@user_bp.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('user.dashboard'))
