from flask import Blueprint, jsonify, request

bp = Blueprint('users', __name__, url_prefix="/users")

@bp.route('/', methods=['GET'])
def get_all_users():
    from . import db
    return jsonify(db.users), 200

@bp.route("/<int:id>")
def get_user(id):
    users_found = _get_users_by_id(id)

    if (len(users_found) == 0):
        return jsonify({"error": "User not found"}), 404
    elif (len(users_found) > 1):
        return jsonify({"error": "Multiple users found"}), 500
    else:
        return jsonify(users_found[0]), 200

@bp.route("/", methods=['POST'])
def create_user():
    if 'name' not in request.json or 'lastname' not in request.json:
        return jsonify({"error": "Missing 'name' or 'lastname' fields"}), 400

    created_user = _create_user_from_request(None, request)
    return jsonify(created_user), 201

@bp.route("/<int:id>", methods=['PATCH'])
def update_user(id):
    if 'name' not in request.json and 'lastname' not in request.json:
        return jsonify({"error": "Missing 'name' and 'lastname' fields"}), 400

    users_found = _get_users_by_id(id)
    if (len(users_found) == 0):
        return jsonify({"error": "User not found"}), 404
    elif (len(users_found) > 1):
        return jsonify({"error": "Multiple users found"}), 500
    else:
        _update_user_from_request(users_found[0], request)
    return "", 204

@bp.route("/<int:id>", methods=['PUT'])
def create_or_update_user(id):
    if 'name' not in request.json or 'lastname' not in request.json:
        return jsonify({"error": "Missing 'name' or 'lastname' fields"}), 400

    users_found = _get_users_by_id(id)
    if (len(users_found) == 0):
        _create_user_from_request(id, request)
    elif (len(users_found) > 1):
        return jsonify({"error": "Multiple users found"}), 500
    else:
        _update_user_from_request(users_found[0], request)
    return "", 204

@bp.route("/<int:id>", methods=['DELETE'])
def delete_user(id):
    from . import db
    is_found = False
    index = 0
    for u in db.users:
        if id == u['id']:
            is_found = True
            break
        else:
            index += 1
    if not is_found:
        return jsonify({"error": "User not found"}), 400
    db.users.pop(index)
    return "", 204

def _get_users_by_id(id):
    from . import db
    users_found = []
    for u in db.users:
        if u["id"] == id:
            users_found.append(u)
    return users_found

def _create_user_from_request(id, request):
    from . import db
    name = request.json.get('name')
    lastname = request.json.get('lastname')
    user_id = id
    if id is None:
        current_maximum_id = 0
        for u in db.users:
            if current_maximum_id < u['id']:
                current_maximum_id = u['id']
        user_id = current_maximum_id + 1

    created_user =  {"id": user_id, "name": name, "lastname": lastname}
    db.users.append(created_user)

    return created_user

def _update_user_from_request(user, request):
    if 'name' in request.json:
        user['name'] = request.json.get('name')

    if 'lastname' in request.json:
        user['lastname'] = request.json.get('lastname')