from flask import Blueprint
from flask import request
from flask.views import MethodView

from app.services.person_service import PersonService


class PersonAPI(MethodView):
    def __init__(self):
        super().__init__()
        self.person_service = PersonService()

    def get(self, person_id):
        try:
            if person_id is not None:
                result = self.person_service.get(person_id)
            else:
                result = self.person_service.list()

            return {"data": result}
        except Exception:
            return {"data": None}, 404

    def post(self):
        result = self.person_service.create(request.form.get("name"),
                                            request.files.get("image").read())

        return {"data": result}

    def put(self, person_id):
        print("put", person_id)
        # update & delete face
        pass

    def delete(self, person_id):
        total_rows = self.person_service.delete(person_id)

        return {
            "data": {"total_rows": total_rows}
        }


view = PersonAPI.as_view("person")

blueprint = Blueprint("person", __name__)
blueprint.add_url_rule("/api/people", view_func=view, methods=["GET"], defaults={"person_id": None})
blueprint.add_url_rule("/api/people", view_func=view, methods=["POST"])
blueprint.add_url_rule("/api/people/<int:person_id>", view_func=view, methods=["GET", "PUT", "DELETE"])
