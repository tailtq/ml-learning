import os
from pathlib import Path

import cv2
import pickle
import numpy as np
from image2face import ArcfacePrediction, RetinafacePrediction

face_detection = RetinafacePrediction("mobile0.25", use_cpu=True)
face_recognition = ArcfacePrediction("resnet50", use_cpu=True)

pickle_path = Path(__file__).parent / "faces.pickle"


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
        feature_vectors = load_pickle(pickle_path)

    feature_vectors[name] = feature_vector
    save_pickle(pickle_path, feature_vectors)

    print("Save face successfully!")


def save_pickle(file_path, data):
    with open(file_path, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(file_path):
    with open(file_path, "rb") as handle:
        data = pickle.load(handle)

    return data


if __name__ == "__main__":
    save_facial_vector("Musk", "./samples/Musk.jpeg")
    save_facial_vector("Tai", "./samples/Tai.jpg")
    save_facial_vector("Bau", "./samples/Bau.png")
    save_facial_vector("Thai", "./samples/Thai.jpeg")
