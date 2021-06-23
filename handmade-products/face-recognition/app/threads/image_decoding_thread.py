import cv2
import time
import queue
from app.configs.video_config import VideoConfig, ProcessStatus
from app.threads.base_thread import BaseThread


class ImageDecodingThread(BaseThread):
    def __init__(self,
                 url,
                 video_config: VideoConfig,
                 process_status: ProcessStatus,
                 detecting_queue: queue.Queue):
        super().__init__()

        self.url = url
        self.video_config = video_config
        self.process_status = process_status
        self.detecting_queue = detecting_queue

    def _run(self):
        """
        Run the stream and push each frame into a queue
        :return:
        """
        print(f"ImageDecodingThread is running")

        index = 0
        stream = self._load_stream()
        drop_last_frame_in_n_steps = self.video_config.drop_last_frame_in_n_steps

        start_time = time.time()

        while True:
            if self.process_status.image_decoding_status:
                break

            if self.detecting_queue.qsize() >= self.video_config.max_queue_size:
                time.sleep(0.001)
                continue

            have_frame = stream.grab()

            if not have_frame:
                break

            index += 1

            # ignore the last frame in n steps
            if index % drop_last_frame_in_n_steps == 0:
                continue

            # decode frame
            _, frame = stream.retrieve()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # put image to queue to be handled at another thread
            self.detecting_queue.put({
                "frame_index": index,
                "frame": frame,
            })

        # print performance time
        print(f"{self.__class__.__name__}: {time.time() - start_time}")

        # set status for this thread
        self.process_status.image_decoding_status = True
        # close the connection to the device or video file
        stream.release()

    def _load_stream(self):
        """
        Load video stream from url
        :return: cv2.VideoCapture
        """
        stream = cv2.VideoCapture(self.url)

        # set fourcc before width and height
        stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        return stream
