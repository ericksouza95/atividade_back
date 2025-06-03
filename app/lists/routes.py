from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import TaskList
from .. import db

list_bp = Blueprint('list', __name__, url_prefix='/lists')

@list_bp.route('/', methods=['GET'])
@login_required
def get_lists():
    lists = TaskList.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': l.id, 'name': l.name} for l in lists])

@list_bp.route('/', methods=['POST'])
@login_required
def create_list():
    data = request.get_json()
    new_list = TaskList(name=data['name'], user_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()
    return jsonify({'message': 'Lista criada'}), 201

@list_bp.route('/<int:list_id>', methods=['PUT'])
@login_required
def update_list(list_id):
    data = request.get_json()
    task_list = TaskList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    task_list.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Lista atualizada'})

@list_bp.route('/<int:list_id>', methods=['DELETE'])
@login_required
def delete_list(list_id):
    task_list = TaskList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    db.session.delete(task_list)
    db.session.commit()
    return jsonify({'message': 'Lista removida'})
