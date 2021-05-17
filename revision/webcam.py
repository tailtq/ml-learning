import cv2
import time

stream = cv2.VideoCapture(0)
# set fourcc before width and height
stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

fps = 0
start_time = time.time()

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

    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Test", frame)
    key = cv2.waitKey(10)

    if key == ord("q"):
        break

stream.release()
cv2.destroyAllWindows()
