from dotenv import dotenv_values
from datetime import datetime

from app.utils.db_persistence_utils import DBPersistenceUtils


class AttendanceDBPersistence(DBPersistenceUtils):
    def __init__(self):
        env_config = dotenv_values(".env")
        super().__init__(env_config["DATABASE_PATH"], "attendances")

    def delete_by_person(self, person_id):
        return self.delete_by_condition({"person_id": person_id})

    def is_attended_today(self, person_id):
        current_date = datetime.now().strftime("%Y-%m-%d")

        con = self._generate_connection()

        cur = con.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE date(substr(attended_at, 0, 11)) = date(?) AND person_id = ?", (current_date, person_id))
        # get data
        values = cur.fetchone()

        cur.close()
        con.close()

        return True if values else False
