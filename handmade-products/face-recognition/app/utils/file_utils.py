import cv2
import time


class FileUtils:
    def save_image(self, image, local_path: str, extension: str = ".jpg"):
        """
        Save local storage image
        :param extension: string
        :param image: numpy array
        :param local_path: string
        :return:
        """
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imwrite(f"{local_path}/{self._generate_file_name()}{extension}", image)

    @staticmethod
    def _generate_file_name():
        return str(int(time.time() * 1000))
