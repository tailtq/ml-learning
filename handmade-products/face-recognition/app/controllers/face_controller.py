from flask import Blueprint

blueprint = Blueprint("face", __name__, url_prefix="/api/faces")


def save_facial_vector(name, image):
    detections = face_detection.predict(image)

    assert len(detections) != 0

    widths = detections[:, 2] - detections[:, 0]
    detection = detections[widths.argmax()]
    aligned_face = face_detection.align_face(image, detection, width=112, height=112)

    # norm_face = np.zeros(aligned_face.shape)
    # cv2.normalize(aligned_face, norm_face, 0, 255, cv2.NORM_MINMAX)
    # feature_vector = face_recognition.predict(norm_face)
    feature_vector = face_recognition.predict(aligned_face)

    feature_vectors = {}

    if os.path.exists(pickle_path):
        feature_vectors = pickle_utils.load_pickle(pickle_path)

    feature_vectors[name] = feature_vector
    pickle_utils.save_pickle(pickle_path, feature_vectors)

    print("Save face successfully!")


@blueprint.route("/", methods=["POST"])
def add_face():
    return {
        "status": True,
        "message": "OK",
        "data": "123"
    }


def update_face(id):
    pass

