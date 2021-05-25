import cv2
import time
import numpy as np
from scipy.spatial import distance
from save_face import load_pickle, pickle_path
from image2face import RetinafacePrediction, ArcfacePrediction

stream = cv2.VideoCapture("http://192.168.1.54:4747/video")
# set fourcc before width and height
stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

fps = 0
start_time = time.time()
face_detection = RetinafacePrediction("mobile0.25", use_cpu=True)
face_recognition = ArcfacePrediction("resnet50", use_cpu=True)

feature_vectors = load_pickle(pickle_path)
names = list(feature_vectors.keys())
feature_vectors = np.array(list(feature_vectors.values()))
print(names)

while True:
    _, frame = stream.read()

    if frame is None:
        break

    fps += 1

    if time.time() - start_time >= 1:
        # calculate fps
        print(f"FPS: {fps}")
        print("---" * 10)
        # reset
        fps = 0
        start_time = time.time()

    detections = face_detection.predict(frame)

    for detection in detections:
        # align face and extract feature vector
        aligned_face = face_detection.align_face(frame, detection)
        face_feature_vector = face_recognition.predict(aligned_face)

        # calculate Euclidean distance
        distances = np.sqrt(np.square(face_feature_vector - feature_vectors).sum(axis=1))
        closest_face_index = distances.argmin()

        print(f"Distance: {distances[closest_face_index]}")

        detection = list(map(int, detection))
        # draw bounding box
        cv2.rectangle(frame, (detection[0], detection[1]), (detection[2], detection[3]), (0, 0, 255), 2)

        # write name to object
        cx = detection[0]
        cy = detection[1] - 24
        cv2.putText(frame, names[closest_face_index], (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

        # landms
        cv2.circle(frame, (detection[5], detection[6]), 1, (0, 0, 255), 4)
        cv2.circle(frame, (detection[7], detection[8]), 1, (0, 255, 255), 4)
        cv2.circle(frame, (detection[9], detection[10]), 1, (255, 0, 255), 4)
        cv2.circle(frame, (detection[11], detection[12]), 1, (0, 255, 0), 4)
        cv2.circle(frame, (detection[13], detection[14]), 1, (255, 0, 0), 4)

    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Test", frame)
    key = cv2.waitKey(10)

    if key == ord("q"):
        break

stream.release()
cv2.destroyAllWindows()
