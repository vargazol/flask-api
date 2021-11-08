import json
import redis
from flask import Flask, request, jsonify


app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
response_type = {'Content-Type': 'application/json'}


def flask_api():
    def does_namespace_exist(namespace):
        namespaces = []
        for each_namespace in r.scan_iter():
            namespaces.append(each_namespace)
        if namespace in namespaces:
            return True
        else:
            return False

    @app.route("/", methods=["GET"])
    def list_namespaces():
        namespaces = []
        for namespace in r.scan_iter():
            namespaces.append(namespace)
        namespace_list = jsonify(namespaces)
        return namespace_list, 200, response_type

    @app.route('/<string:namespace>', methods=["GET"])
    def get_namespace(namespace):
        if does_namespace_exist(namespace) == False:
            return {"status": "error", "reason": "requested namespace not found"}, 404, response_type
        else:
            response = r.get(namespace)
            namespace_content = response.replace("'", "\"")
        return namespace_content, 200, response_type

    @ app.route('/<string:namespace>', methods=["PUT"])
    def create_namespace(namespace):
        if does_namespace_exist(namespace):
            return {"created": False, "reason": "namespace already exists"}, 409, response_type
        else:
            new_namespace = request.get_json()
            r.set(namespace, f"{new_namespace}")
        return {"created": True, "namespace": namespace}, 201, response_type

    @app.route('/<string:namespace>', methods=["POST"])
    def update_namespace(namespace):
        if does_namespace_exist(namespace) == False:
            return {"updated": False, "reason": "requested namespace not found"}, 404, response_type
        else:
            original_namespace = r.get(namespace).replace("'", "\"")
            response = json.loads(original_namespace)
            new_data = request.get_json()
            modified_namespace = response | new_data
            r.set(namespace, f"{modified_namespace}")
        return modified_namespace, 200, response_type

    @ app.route('/<string:namespace>', methods=["DELETE"])
    def delete_namespace(namespace):
        if does_namespace_exist(namespace) == False:
            return {"deleted": False, "reason": "requested namespace not found"}, 404, response_type
        else:
            r.delete(namespace)
        return {"deleted": True, "namespace": namespace}, 200, response_type

    return app
