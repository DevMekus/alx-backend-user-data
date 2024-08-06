#!/usr/bin/env python3
"""User view models.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    """
    allUsers = [user.to_json() for user in User.all()]
    return jsonify(allUsers)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
      - User ID.
    Return:
      - empty JSON is the User has been correctly deleted.
      - 404 if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/    
    """
    requestJson = None
    errMessage = None
    try:
        requestJson = request.get_json()
    except Exception as e:
        requestJson = None
    if requestJson is None:
        errMessage = "Wrong format"
    if errMessage is None and requestJson.get("email", "") == "":
        errMessage = "email missing"
    if errMessage is None and requestJson.get("password", "") == "":
        errMessage = "password missing"
    if errMessage is None:
        try:
            user = User()
            user.email = requestJson.get("email")
            user.password = requestJson.get("password")
            user.first_name = requestJson.get("first_name")
            user.last_name = requestJson.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            errMessage = "Can't create User: {}".format(e)
    return jsonify({'error': errMessage}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    requestJson = None
    try:
        requestJson = request.get_json()
    except Exception as e:
        requestJson = None
    if requestJson is None:
        return jsonify({'error': "Wrong format"}), 400
    if requestJson.get('first_name') is not None:
        user.first_name = requestJson.get('first_name')
    if requestJson.get('last_name') is not None:
        user.last_name = requestJson.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200