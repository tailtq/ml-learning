import cv2
import time
import numpy as np
import imutils
from config import CONFIG, face_detection, face_recognition

# "http://192.168.1.54:4747/video"
video_path = "musk_test.mp4"
stream = cv2.VideoCapture(video_path)
# set fourcc before width and height
stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

fps = 0
start_time = time.time()

frame_counter = 0

while True:
    _, frame = stream.read()

    if frame is None:
        break

    if CONFIG["DROP_FRAME_AFTER_STEP"] == -1 and frame_counter % CONFIG["DROP_FRAME_AFTER_STEP"] == 0:
        continue

    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame_counter += 1
    fps += 1
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if time.time() - start_time >= 1:
        # calculate fps
        print(f"FPS: {fps}")
        print("---" * 10)
        # reset
        fps = 0
        start_time = time.time()

    detections = face_detection.predict(frame)

    for index, detection in enumerate(detections):
        if detection[0] < 0 or detection[1] < 0 or detection[2] < 0 or detection[3] < 0:
            continue

        # align face and extract feature vector
        aligned_face = face_detection.align_face(frame, detection)
        detection = list(map(int, detection))

        cv2.imshow(f"Test_{index}", aligned_face)
        face_feature_vector = face_recognition.predict(aligned_face)

        # # calculate Euclidean distance
        distances = np.sqrt(np.square(face_feature_vector - CONFIG["FACES"]["VECTORS"]).sum(axis=1))
        closest_face_index = distances.argmin()

        if distances[closest_face_index] < CONFIG["THRESHOLD"]:
            print(f"{CONFIG['FACES']['NAMES'][closest_face_index]}: {distances[closest_face_index]}")
            # write name to object
            cx = detection[0]
            cy = detection[1] - 24
            cv2.putText(frame, CONFIG["FACES"]["NAMES"][closest_face_index], (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255), 2)

        # draw bounding box
        cv2.rectangle(frame, (detection[0], detection[1]), (detection[2], detection[3]), (0, 0, 255), 2)

        # landmarks
        cv2.circle(frame, (detection[5], detection[6]), 1, (0, 0, 255), 4)
        cv2.circle(frame, (detection[7], detection[8]), 1, (0, 255, 255), 4)
        cv2.circle(frame, (detection[9], detection[10]), 1, (255, 0, 255), 4)
        cv2.circle(frame, (detection[11], detection[12]), 1, (0, 255, 0), 4)
        cv2.circle(frame, (detection[13], detection[14]), 1, (255, 0, 0), 4)

    frame = imutils.resize(frame, width=640)
    cv2.imshow("Test", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    key = cv2.waitKey(10)

    if key == ord("q"):
        break

stream.release()
cv2.destroyAllWindows()
