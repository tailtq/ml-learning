from dotenv import dotenv_values

from app.utils.db_persistence_utils import DBPersistenceUtils


env_config = dotenv_values(".env")


class AttendanceDBPersistence(DBPersistenceUtils):
    def __init__(self):
        super().__init__(env_config["DATABASE_PATH"], "attendances")

    def delete_by_person(self, person_id):
        return self.delete_by_condition({"person_id": person_id})
