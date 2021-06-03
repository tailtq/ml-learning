import time
import queue
from configs.video_config import VideoConfig, ProcessStatus
from threads.base_thread import BaseThread


class TrackingThread(BaseThread):
    def __init__(self,
                 video_config: VideoConfig,
                 process_status: ProcessStatus,
                 tracking_queue: queue.Queue):
        super().__init__()

        self.video_config = video_config
        self.process_status = process_status
        self.tracking_queue = tracking_queue

    def _run(self):
        """
        Run the stream and push each frame into a queue
        :return:
        """
        print(f"TrackingThread is running")
        print("---" * 30)

        while True:
            if self.tracking_queue.empty():
                time.sleep(0.0001)
                continue

            queue_data = self.tracking_queue.get()
            print(queue_data["faces"])
