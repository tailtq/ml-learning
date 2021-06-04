import os
import cv2
import utils.pickle_utils as pickle_utils
from configs.models import face_detection, face_recognition

pickle_path = "./faces.pickle"


def save_facial_vector(name, image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detections = face_detection.predict(image)

    assert len(detections) != 0

    widths = detections[:, 2] - detections[:, 0]
    detection = detections[widths.argmax()]
    aligned_face = face_detection.align_face(image, detection)
    feature_vector = face_recognition.predict(aligned_face)

    feature_vectors = {}

    if os.path.exists(pickle_path):
        feature_vectors = pickle_utils.load_pickle(pickle_path)

    feature_vectors[name] = feature_vector
    pickle_utils.save_pickle(pickle_path, feature_vectors)

    print("Save face successfully!")


if __name__ == "__main__":
    save_facial_vector("Musk", "./samples/Musk.jpeg")
    save_facial_vector("Tai", "./samples/Tai.jpg")
    save_facial_vector("Bau", "./samples/Bau.png")
    save_facial_vector("Thai", "./samples/Thai.jpeg")
