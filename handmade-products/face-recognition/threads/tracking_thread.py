import time
import queue
from sort.sort import *
from configs.video_config import VideoConfig, ProcessStatus
from threads.base_thread import BaseThread


class TrackingThread(BaseThread):
    def __init__(self,
                 video_config: VideoConfig,
                 process_status: ProcessStatus,
                 tracking_queue: queue.Queue,
                 visualization_queue: queue.Queue):
        super().__init__()

        self.video_config = video_config
        self.process_status = process_status
        self.tracking_queue = tracking_queue
        self.visualization_queue = visualization_queue
        self.tracker = Sort()

    def _run(self):
        """
        Run the stream and push each frame into a queue
        :return:
        """
        print(f"TrackingThread is running")

        while True:
            if self.tracking_queue.empty():
                # stop tracking process if queue is empty and detecting status is done
                if self.process_status.detecting_status:
                    break

                time.sleep(0.0001)
                continue

            queue_data = self.tracking_queue.get()
            faces = queue_data["faces"][:, :4]

            tracks = self.tracker.update(faces)

            self.visualization_queue.put({
                "tracks": tracks,
                "frame": queue_data["frame"]
            })
            # apply face recognition

        self.process_status.tracking_status = True
