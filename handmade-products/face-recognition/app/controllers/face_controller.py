from flask import Blueprint

blueprint = Blueprint("face", __name__, url_prefix="/api/faces")


@blueprint.route("/", methods=["POST"])
def add_face():
    return {
        "status": True,
        "message": "OK",
        "data": "123"
    }


def update_face(id):
    pass

