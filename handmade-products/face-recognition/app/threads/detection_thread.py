import time
import queue

from app.configs.models import face_detection
from app.configs.video_config import ProcessStatus, VideoConfig
from app.threads.base_thread import BaseThread


class DetectionThread(BaseThread):
    def __init__(self,
                 video_config: VideoConfig,
                 process_status: ProcessStatus,
                 detecting_queue: queue.Queue,
                 tracking_queue: queue.Queue):
        super().__init__()

        self.video_config = video_config
        self.process_status = process_status
        self.detecting_queue = detecting_queue
        self.tracking_queue = tracking_queue

    def _run(self):
        print(f"DetectionThread is running")

        while True:
            if self.tracking_queue.qsize() > self.video_config.max_queue_size:
                time.sleep(0.001)
                continue

            if not self.detecting_queue.empty():
                queue_data = self.detecting_queue.get()
                faces = face_detection.predict(queue_data["frame"], width=self.video_config.detection_size)

                self.tracking_queue.put({
                    **queue_data,
                    "faces": faces
                })
            elif self.process_status.image_decoding_status and self.detecting_queue.empty():
                # set status for this thread
                break

        self.process_status.detecting_status = True
