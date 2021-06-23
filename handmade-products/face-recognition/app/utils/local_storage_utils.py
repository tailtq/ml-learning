import cv2
import os

from app.utils.random_utils import random_string_with_datetime


class LocalStorageUtils:
    @staticmethod
    def save_image(image, local_path, extension="jpg"):
        """

        """
        os.makedirs(local_path, exist_ok=True)

        file_name = random_string_with_datetime(4) + "." + extension
        file_path = f"{local_path}/{file_name}" if local_path else file_name

        cv2.imwrite(file_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        return file_path
