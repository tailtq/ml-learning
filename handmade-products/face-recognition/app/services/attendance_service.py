from dotenv import dotenv_values
from datetime import datetime

from app.utils.db_persistence_utils import DBPersistenceUtils


class AttendanceService:
    def __init__(self):
        self.attendance_db_persistence = AttendanceDBPersistence()

    def list_by_date(self, date: str):
        return self.attendance_db_persistence.list_by_date(date)


class AttendanceDBPersistence(DBPersistenceUtils):
    def __init__(self):
        env_config = dotenv_values(".env")
        super().__init__(env_config["DATABASE_PATH"], "attendances")

    def delete_by_person(self, person_id):
        return self.delete_by_condition({"person_id": person_id})

    def is_attended_today(self, person_id):
        current_date = datetime.now().strftime("%Y-%m-%d")
        query = f"SELECT * FROM {self.table_name} WHERE date(substr(attended_at, 0, 11)) = date(?) AND person_id = ?"

        result = self._fetchone(query, [current_date, person_id])

        return True if result else False

    def list_by_date(self, date):
        query = f"SELECT * FROM {self.table_name} WHERE date(substr(attended_at, 0, 11)) = date(?) order by attended_at"
        result = self._fetchall(query, [date])

        return result
