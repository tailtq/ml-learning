from flask.views import View
from flask.blueprints import Blueprint
from flask.globals import request

from app.services.process_service import ProcessService


class ProcessController(View):
    methods = ["POST"]

    def __init__(self):
        self.process_service = ProcessService()

    def dispatch_request(self, action):
        result = {}

        if action == "start":
            result["process_id"] = self.process_service.start_process()
        elif action == "stop":
            process_id = request.args.get("id")

            try:
                self.process_service.stop_process(process_id)
            except:
                return {"data": None}, 404

        return result


blueprint = Blueprint("process", __name__)
blueprint.add_url_rule("/api/processes/<action>", view_func=ProcessController.as_view("process"))
