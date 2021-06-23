import time
import queue
import cv2
import imutils

import app.utils.drawing_utils as drawing_utils
from app.configs.video_config import VideoConfig, ProcessStatus
from app.services.person_service import PersonPicklePersistence
from app.threads import ImageDecodingThread, DetectionThread, TrackingThread
from app.threads.base_thread import BaseThread
from app.utils.random_utils import random_string_with_datetime
from app.utils.singleton_utils import SingletonMeta


class ProcessService(metaclass=SingletonMeta):
    def __init__(self):
        self.main_threads = {}

    def start_process(self):
        process_id = random_string_with_datetime()

        tracking_process = TrackingProcess(process_id)
        tracking_process.run_thread()
        self.main_threads[process_id] = tracking_process

        return process_id

    def stop_process(self, process_id):
        if process_id not in self.main_threads:
            raise Exception("resource_not_found")

        self.main_threads[process_id].stop()
        del self.main_threads[process_id]


class TrackingProcess(BaseThread):
    def __init__(self, process_id):
        super().__init__()
        self.process_id = process_id
        self.video_config = VideoConfig(drop_last_frame_in_n_steps=2)
        self.process_status = ProcessStatus()

        # define queues for image decoding, tracking, and visualization thread
        self.detecting_queue = queue.Queue()
        self.tracking_queue = queue.Queue()
        self.visualization_queue = queue.Queue()

    def _run(self):
        person_ids, _, facial_vectors = PersonPicklePersistence().load_information()

        try:
            image_decoding_thread = ImageDecodingThread("samples/tai.mp4",
                                                        self.video_config,
                                                        self.process_status,
                                                        self.detecting_queue)
            image_decoding_thread.run_thread()
            self.child_threads.append(image_decoding_thread)

            detecting_thread = DetectionThread(self.video_config,
                                               self.process_status,
                                               self.detecting_queue,
                                               self.tracking_queue)
            detecting_thread.run_thread()
            self.child_threads.append(detecting_thread)

            tracking_thread = TrackingThread(facial_vectors,
                                             person_ids,
                                             self.video_config,
                                             self.process_status,
                                             self.tracking_queue,
                                             self.visualization_queue)
            tracking_thread.run_thread()
            self.child_threads.append(tracking_thread)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        # set all status done & empty queue to remove child threads
        self.process_status.image_decoding_status = True
        self.process_status.detecting_status = True
        self.process_status.tracking_status = True

        self.detecting_queue.queue.clear()
        self.tracking_queue.queue.clear()
        self.visualization_queue.queue.clear()

    # def visualize(self):
    #     while not (self.process_status.tracking_status and self.visualization_queue.empty()):
    #         if self.visualization_queue.empty():
    #             time.sleep(0.01)
    #             continue
    #
    #         queue_data = self.visualization_queue.get()
    #         frame, tracks = queue_data["frame"], queue_data["tracks"]
    #         frame = drawing_utils.draw_tracks(frame, tracks)
    #
    #         # frame = cv2.resize(frame, (640, 480))
    #         # cv2.imshow(self.process_id, frame)
    #         cv2.waitKey(10)
    #
    #     cv2.destroyAllWindows()
