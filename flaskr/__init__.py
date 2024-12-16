import os

from flask import Flask, jsonify, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World! My name is Anton.'
    
    @app.route('/users', methods=['GET'])
    def get_all_users():
        from . import db
        return jsonify(db.users), 200
    
    @app.route("/users/<id>")
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
    
    @app.route("/users", methods=['POST'])
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
    
    @app.route("/users/<int:id>", methods=['DELETE'])
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


    return app