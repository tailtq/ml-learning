import cv2
import sys
import imutils
import numpy as np
from config import CONFIG, face_detection, face_recognition


if __name__ == "__main__":
    image_path = sys.argv[1]

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    detections = face_detection.predict(image)

    for index, detection in enumerate(detections):
        if detection[0] < 0 or detection[1] < 0 or detection[2] < 0 or detection[3] < 0:
            continue

        # align face and extract feature vector
        aligned_face = face_detection.align_face(image, detection, width=112, height=112)
        detection = list(map(int, detection))
        cv2.imshow(f"Image{index}", cv2.cvtColor(aligned_face, cv2.COLOR_RGB2BGR))

        face_feature_vector = face_recognition.predict(aligned_face)

        # # calculate Euclidean distance
        distances = np.sqrt(np.square(face_feature_vector - CONFIG["FACES"]["VECTORS"]).sum(axis=1))
        closest_face_index = distances.argmin()

        for index, distance in enumerate(distances):
            print(f"Name --- {CONFIG['FACES']['NAMES'][index]}: {distance}")

        if distances[closest_face_index] < 0.1:
            print(f"Result --- {CONFIG['FACES']['NAMES'][closest_face_index]}: {distances[closest_face_index]}")
            # write name to object
            cx = detection[0]
            cy = detection[1] - 24
            cv2.putText(image, CONFIG["FACES"]["NAMES"][closest_face_index], (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (255, 255, 255), 2)

        # draw bounding box
        cv2.rectangle(image, (detection[0], detection[1]), (detection[2], detection[3]), (0, 0, 255), 2)

        # landmarks
        cv2.circle(image, (detection[5], detection[6]), 1, (0, 0, 255), 4)
        cv2.circle(image, (detection[7], detection[8]), 1, (0, 255, 255), 4)
        cv2.circle(image, (detection[9], detection[10]), 1, (255, 0, 255), 4)
        cv2.circle(image, (detection[11], detection[12]), 1, (0, 255, 0), 4)
        cv2.circle(image, (detection[13], detection[14]), 1, (255, 0, 0), 4)
        print("---")

    image = imutils.resize(image, width=640)
    cv2.imshow("Test", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    key = cv2.waitKey(-1)
    
cv2.destroyAllWindows()
