from app.configs.models import face_detection, face_recognition


def extract_facial_vector(image):
    detections = face_detection.predict(image)

    if len(detections) == 0:
        raise Exception('image_has_no_face')

    assert len(detections) != 0

    widths = detections[:, 2] - detections[:, 0]

    detection = detections[widths.argmax()]
    aligned_face = face_detection.align_face(image, detection, width=112, height=112)
    feature_vector = face_recognition.predict(aligned_face)

    return aligned_face, feature_vector



def save_facial_vector_to_sqlite(name, image):
    aligned_face, feature_vector = extract_facial_vector(image)

    # save aligned_face to local storage
    # save (name, avatar, facial_vector) to SQL Lite
    

    # norm_face = np.zeros(aligned_face.shape)
    # cv2.normalize(aligned_face, norm_face, 0, 255, cv2.NORM_MINMAX)
    # feature_vector = face_recognition.predict(norm_face)

    feature_vectors = {}

    if os.path.exists(pickle_path):
        feature_vectors = pickle_utils.load_pickle(pickle_path)

    feature_vectors[name] = feature_vector
    pickle_utils.save_pickle(pickle_path, feature_vectors)
