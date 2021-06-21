import io
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
from dotenv import dotenv_values

from app.configs.models import face_detection, face_recognition
from app.services.attendance_service import AttendanceDBPersistence
from app.utils.pickle_utils import load_pickle, save_pickle
from app.utils.db_persistence_utils import DBPersistenceUtils
from app.utils.local_storage_utils import LocalStorageUtils

env_config = dotenv_values(".env")

pickle_file_path = "./storage/faces.pickle"
avatar_local_storage = "public/img"


class PersonService:
    def __init__(self):
        self.person_db_persistence = PersonDBPersistence()
        self.person_pickle_persistence = PersonPicklePersistence(pickle_file_path)

        self.attendance_db_persistence = AttendanceDBPersistence()

    def list(self):
        result = self.person_db_persistence.find()

        return result

    def get(self, person_id):
        result = self.person_db_persistence.find_one(person_id)

        if not result:
            raise Exception("resource_not_found")

        return result

    def create(self, name, image_binary):
        """
        Save information to database & local storage & pickle file
        :param name:
        :param image_binary:
        :return:
        """
        image = self._convert_binary_to_numpy(image_binary)

        # align face and extract facial vector
        aligned_face, facial_vector = self._extract_facial_vector(image)
        avatar_path = LocalStorageUtils.save_image(aligned_face, avatar_local_storage)

        # insert data to database
        person_id = self.person_db_persistence.create({
            "name": name,
            "avatar": avatar_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        # insert face to pickle files
        self.person_pickle_persistence.save_person(person_id, list(facial_vector))

        return self.person_db_persistence.find_one(person_id)

    def delete(self, person_id):
        # delete attendances relationship
        self.attendance_db_persistence.delete_by_person(person_id)
        # delete row and data in pickle file
        total_rows = self.person_db_persistence.delete(person_id)
        self.person_pickle_persistence.delete_person(person_id)

        return total_rows

    def _extract_facial_vector(self, image):
        """
        Rotate face and extract facial vector
        :param image:
        :return:
        """
        detections = face_detection.predict(image)

        if len(detections) == 0:
            raise Exception("image_has_no_face")

        widths = detections[:, 2] - detections[:, 0]
        detection = detections[widths.argmax()]

        aligned_face = face_detection.align_face(image, detection)
        resized_face = cv2.resize(aligned_face, (112, 112))
        feature_vector = face_recognition.predict(resized_face)

        return aligned_face, feature_vector

    def _convert_binary_to_numpy(self, image_binary):
        """

        :param image_binary:
        :return:
        """
        image = io.BytesIO(image_binary)
        image = Image.open(image)
        image = np.asarray(image)

        return image


class PersonDBPersistence(DBPersistenceUtils):
    def __init__(self):
        super().__init__(env_config["DATABASE_PATH"], "people")


class PersonPicklePersistence:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_person(self, person_id, vector):
        """
        Create person & add face to pickle file
        :param person_id:
        :param vector:
        :return:
        """
        people = load_pickle(self.file_path, {})
        
        if person_id not in people:
            people[person_id] = [vector]
        else:
            people[person_id].append(vector)
            
        save_pickle(self.file_path, people)

        return None

    def delete_person(self, person_id):
        """
        Delete person from pickle file
        :param person_id:
        :return:
        """
        people = load_pickle(self.file_path, {})

        if person_id in people:
            del people[person_id]

        save_pickle(self.file_path, people)

        return None
