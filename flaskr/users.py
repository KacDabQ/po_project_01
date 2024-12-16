from flask import Blueprint, jsonify, request

bp = Blueprint('users', __name__, url_prefix="/users")

@bp.route('/', methods=['GET'])
def get_all_users():
    from . import db
    return jsonify(db.users), 200

@bp.route("/<id>")
def get_user(id):
    from . import db
    users_found = []
    for u in db.users:
        if str(u["id"]) == id:
            users_found.append(u)

    if (len(users_found) == 0):
        return jsonify({"error": "User not found"}), 404
    elif (len(users_found) > 1):
        return jsonify({"error": "Multiple users found"}), 500
    else:
        return jsonify(users_found[0]), 200

@bp.route("/", methods=['POST'])
def create_user():
    from . import db
    name = request.json.get('name')
    lastname = request.json.get('lastname')
    current_maximum_id = 0
    for u in db.users:
        if current_maximum_id < u['id']:
            current_maximum_id = u['id']
    created_user = {"id": current_maximum_id + 1, "name": name, "lastname": lastname}
    db.users.append(created_user)
    return jsonify(created_user), 201

@bp.route("/<int:id>", methods=['DELETE'])
def delete_user(id):
    from . import db
    index = 0
    for u in db.users:
        if id == u['id']:
            break
        else:
            index += 1
    db.users.pop(index)
    return str(index)
