import queue

from configs.models import face_detection
from configs.video_config import ProcessStatus
from threads.base_thread import BaseThread


class DetectionThread(BaseThread):
    def __init__(self,
                 process_status: ProcessStatus,
                 image_decoding_queue: queue.Queue,
                 tracking_queue: queue.Queue):
        super().__init__()

        self.process_status = process_status
        self.image_decoding_queue = image_decoding_queue
        self.tracking_queue = tracking_queue

    def _run(self):
        print(f"DetectionThread is running")
        print("---" * 30)

        while True:
            if not self.image_decoding_queue.empty():
                frame_index, frame = self.image_decoding_queue.get()
                faces = face_detection.predict(frame, width=480)
                print(frame_index, faces.shape)
                # print(faces)
            elif self.process_status.image_decoding_status and self.image_decoding_queue.empty():
                # set status for this thread
                self.process_status.detecting_status = True
                break
