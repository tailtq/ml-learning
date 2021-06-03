import time
import queue
from threads import ImageDecodingThread, DetectionThread
from configs.video_config import VideoConfig, ProcessStatus


if __name__ == "__main__":
    video_config = VideoConfig(drop_last_frame_in_n_steps=2)
    process_status = ProcessStatus()
    image_decoding_queue = queue.Queue()
    tracking_queue = queue.Queue()

    image_decoding_thread = ImageDecodingThread("./test_samples/20210528_083812.mp4",
                                                video_config,
                                                process_status,
                                                image_decoding_queue)
    image_decoding_thread.run_thread()

    detection_n_recognition_thread = DetectionThread(process_status,
                                                     image_decoding_queue,
                                                     tracking_queue)
    detection_n_recognition_thread.run_thread()

    while not process_status.image_decoding_status or not process_status.detecting_status:
        time.sleep(0.1)

# stream = cv2.VideoCapture("./test_samples/20210528_083812.mp4")
# # set fourcc before width and height
# stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
# stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#
# while True:
#     start_time = time.time()
#     _, frame = stream.read()
#     print(f"Hello world: {time.time() - start_time}")
