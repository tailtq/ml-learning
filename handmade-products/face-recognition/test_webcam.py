import time
import queue
import cv2

import utils.drawing_utils as drawing_utils
from configs.video_config import VideoConfig, ProcessStatus
from configs.models import feature_vectors
from threads import ImageDecodingThread, DetectionThread, TrackingThread


def visualize(process_status, visualization_queue):
    while not (process_status.tracking_status and visualization_queue.empty()):
        if visualization_queue.empty():
            time.sleep(0.001)
            continue

        queue_data = visualization_queue.get()
        frame, tracks = queue_data["frame"], queue_data["tracks"]

        frame = drawing_utils.draw_tracks(frame, tracks)

        cv2.imshow("Window", frame)
        cv2.waitKey(20)


if __name__ == "__main__":
    video_config = VideoConfig(drop_last_frame_in_n_steps=2)
    process_status = ProcessStatus()

    # define queues for image decoding, tracking, and visualization thread
    detecting_queue = queue.Queue()
    tracking_queue = queue.Queue()
    visualization_queue = queue.Queue()

    try:
        image_decoding_thread = ImageDecodingThread(0,
                                                    video_config,
                                                    process_status,
                                                    detecting_queue)
        image_decoding_thread.run_thread()

        detecting_thread = DetectionThread(video_config, process_status, detecting_queue, tracking_queue)
        detecting_thread.run_thread()

        tracking_thread = TrackingThread(feature_vectors,
                                         video_config,
                                         process_status,
                                         tracking_queue,
                                         visualization_queue)
        tracking_thread.run_thread()

        visualize(process_status, visualization_queue)
    except KeyboardInterrupt:
        detecting_queue.queue.clear()
        tracking_queue.queue.clear()
        visualization_queue.queue.clear()

# import cv2
# from configs.models import face_detection

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
