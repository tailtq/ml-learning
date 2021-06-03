import time
import queue
from threads import ImageDecodingThread, DetectionThread, TrackingThread
from configs.video_config import VideoConfig, ProcessStatus

import cv2
from configs.models import face_detection

if __name__ == "__main__":
    video_config = VideoConfig(drop_last_frame_in_n_steps=2)
    process_status = ProcessStatus()
    image_decoding_queue = queue.Queue()
    tracking_queue = queue.Queue()

    image_decoding_thread = ImageDecodingThread("./test_samples/musk_test.mp4",
                                                video_config,
                                                process_status,
                                                image_decoding_queue)
    image_decoding_thread.run_thread()

    detection_n_recognition_thread = DetectionThread(video_config, process_status, image_decoding_queue, tracking_queue)
    detection_n_recognition_thread.run_thread()

    tracking_thread = TrackingThread(video_config, process_status, tracking_queue)
    tracking_thread.run_thread()

    while not process_status.image_decoding_status or not process_status.detecting_status or not process_status.tracking_status:
        time.sleep(1)


# if __name__ == "__main__":
#     stream = cv2.VideoCapture("./test_samples/20210528_083812.mp4")
#     # set fourcc before width and height
#     stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
#     stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#     stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#
#     while True:
#         start_time = time.time()
#         oke, frame = stream.read()
#
#         if not oke:
#             break
#
#         # face_detection.predict(frame, width=480)
#         print(f"Hello world: {1 / (time.time() - start_time)}")

