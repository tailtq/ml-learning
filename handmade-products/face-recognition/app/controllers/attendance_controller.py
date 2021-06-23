from flask import Blueprint
from flask import request
from flask.views import MethodView
from datetime import datetime

from app.services.attendance_service import AttendanceService


class AttendanceAPI(MethodView):
    def __init__(self):
        super().__init__()
        self.attendance_service = AttendanceService()

    def get(self):
        date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
        print(date)
        result = self.attendance_service.list_by_date(date)

        return {"data": result}


view = AttendanceAPI.as_view("attendance")

blueprint = Blueprint("attendance", __name__)
blueprint.add_url_rule("/api/attendances", view_func=view, methods=["GET"])
