from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from services.item_service import ItemService
from repositories.item_repository import ItemRepository

bp = Blueprint('items', __name__, url_prefix='/items')

repository = ItemRepository()
service = ItemService(repository)


@bp.route("", methods=["GET"])
def index():
    items = service.get_all_items()
    return jsonify([dict(item) for item in items])


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        try:
            service.create_item(title, description)
            return redirect(url_for("items.index"))
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"message": "Send POST with title and description"})


@bp.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id: int):
    item = service.get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        try:
            success = service.update_item(item_id, title, description)
            if success:
                return redirect(url_for("items.index"))
            else:
                return jsonify({"error": "Update failed"}), 500
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    return jsonify(dict(item))


@bp.route("/delete/<int:item_id>", methods=["POST"])
def delete(item_id: int):
    success = service.delete_item(item_id)
    if success:
        return redirect(url_for("items.index"), 303)
    else:
        return jsonify({"error": "Item not found"}), 404


@bp.route("/api/items", methods=["GET"])
def api_get_items():
    items = service.get_all_items()
    return jsonify([dict(item) for item in items])


@bp.route("/api/items/<int:item_id>", methods=["GET"])
def api_get_item(item_id: int):
    item = service.get_item(item_id)
    if item:
        return jsonify(dict(item))
    return jsonify({"error": "Item not found"}), 404


@bp.route("/api/items", methods=["POST"])
def api_create_item():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    title = data.get("title")
    description = data.get("description", "")
    try:
        item_id = service.create_item(title, description)
        return jsonify({"id": item_id, "title": title,
                        "description": description}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/api/items/<int:item_id>", methods=["PUT"])
def api_update_item(item_id: int):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    title = data.get("title")
    description = data.get("description", "")
    try:
        success = service.update_item(item_id, title, description)
        if success:
            return jsonify({"id": item_id, "title": title,
                            "description": description})
        return jsonify({"error": "Item not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/api/items/<int:item_id>", methods=["DELETE"])
def api_delete_item(item_id: int):
    success = service.delete_item(item_id)
    if success:
        return '', 204
    return jsonify({"error": "Item not found"}), 404
