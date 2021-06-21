import io
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
from dotenv import dotenv_values

from app.configs.models import face_detection, face_recognition
from app.utils.db_persistence_utils import DBPersistenceUtils
from app.utils.local_storage_utils import LocalStorageUtils
from app.utils.pickle_utils import load_pickle, save_pickle

env_config = dotenv_values(".env")

pickle_file_path = "./faces.pickle"
avatar_local_storage = "public/img"


class PersonService:
    def __init__(self):
        self.person_db_persistence = PersonDBPersistence()
        self.person_pickle_persistence = PersonPicklePersistence(pickle_file_path)

    def save_face(self, name, image_binary):
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
        super().__init__(env_config["DATABASE_NAME"], "people")


class PersonPicklePersistence:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_person(self, person_id, vector):
        people = load_pickle(self.file_path, {})
        
        if person_id not in people:
            people[person_id] = [vector]
        else:
            people[person_id].append(vector)
            
        save_pickle(self.file_path, people)
