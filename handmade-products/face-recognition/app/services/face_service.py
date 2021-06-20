from app.configs.models import face_detection, face_recognition


class FaceService:
    def extract_facial_vector(self, image):
        detections = face_detection.predict(image)

        if len(detections) == 0:
            raise Exception('image_has_no_face')

        widths = detections[:, 2] - detections[:, 0]
        detection = detections[widths.argmax()]

        aligned_face = face_detection.align_face(image, detection, width=112, height=112)
        feature_vector = face_recognition.predict(aligned_face)

        return aligned_face, feature_vector


