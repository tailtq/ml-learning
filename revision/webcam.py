import cv2
import time
from image2face.retinaface import RetinafaceDetection

stream = cv2.VideoCapture(0)
# set fourcc before width and height
stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

fps = 0
start_time = time.time()
face_detection = RetinafaceDetection("mobile0.25", use_cpu=True)

while True:
    _, frame = stream.read()

    if frame is None:
        break

    fps += 1

    if time.time() - start_time >= 1:
        # calculate fps
        print(f"FPS: {fps}, Shape: {frame.shape}")
        # reset
        fps = 0
        start_time = time.time()

    detections = face_detection.predict(frame)

    for b in detections:
        text = "{:.4f}".format(b[4])
        b = list(map(int, b))
        cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
        cx = b[0]
        cy = b[1] + 12
        cv2.putText(frame, text, (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

        # landms
        cv2.circle(frame, (b[5], b[6]), 1, (0, 0, 255), 4)
        cv2.circle(frame, (b[7], b[8]), 1, (0, 255, 255), 4)
        cv2.circle(frame, (b[9], b[10]), 1, (255, 0, 255), 4)
        cv2.circle(frame, (b[11], b[12]), 1, (0, 255, 0), 4)
        cv2.circle(frame, (b[13], b[14]), 1, (255, 0, 0), 4)

    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Test", frame)
    key = cv2.waitKey(10)

    if key == ord("q"):
        break

stream.release()
cv2.destroyAllWindows()
