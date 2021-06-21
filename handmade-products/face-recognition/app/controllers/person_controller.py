from flask import Blueprint
from flask import request
from flask.views import MethodView

from app.services.person_service import PersonService


class PersonAPI(MethodView):
    def __init__(self):
        super().__init__()
        self.person_service = PersonService()



    def post(self):
        result = self.person_service.save_face(request.form.get("name"),
                                               request.files.get('image').read())

        return result

    def put(self):
        # update & delete face
        pass


blueprint = Blueprint("person", __name__)
blueprint.add_url_rule("/api/people", view_func=PersonAPI.as_view("person"))
