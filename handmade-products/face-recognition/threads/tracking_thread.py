import time
import queue

from sort.sort import *
from configs.models import face_recognition, face_detection
from configs.video_config import VideoConfig, ProcessStatus
from threads.base_thread import BaseThread


class TrackingThread(BaseThread):
    def __init__(self,
                 comparing_faces,
                 video_config: VideoConfig,
                 process_status: ProcessStatus,
                 tracking_queue: queue.Queue,
                 visualization_queue: queue.Queue):
        super().__init__()

        self.comparing_faces = comparing_faces
        self.video_config = video_config
        self.process_status = process_status
        self.tracking_queue = tracking_queue
        self.visualization_queue = visualization_queue
        self.tracker = Sort()
        self.tracks = {}

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
            faces, frame, frame_index = queue_data["faces"], queue_data["frame"], queue_data["frame_index"]

            # update track
            tracks = self.tracker.update(faces)
            current_track_ids = []

            for track in tracks:
                track_id = str(int(track[4]))
                current_track_ids.append(track_id)

                if track_id not in self.tracks:
                    self.tracks[track_id] = {
                        "track_id": track_id,
                        "identity": None,
                        "recognition_time": 0,
                        "appearances": []
                    }

                self.tracks[track_id]["appearances"].append(self._convert_track_format(track, frame, frame_index))

            # apply face recognition
            self.recognize_faces(current_track_ids)
            self.visualization_queue.put({
                "tracks": [self.tracks[track_id] for track_id in current_track_ids],
                "frame": frame,
                "frame_index": frame_index,
            })

        self.process_status.tracking_status = True

    @staticmethod
    def _convert_track_format(track, frame, frame_index):
        """
        Get new format for inserting to SORT algorithm
        :param track:
        :return: tuple
        """
        face = face_detection.align_face(frame, np.concatenate((track[:4], track[5:])))

        return {
            "frame_index": frame_index,
            "box": [track[0], track[1], track[2], track[3]],
            "confidence": track[5],
            "face": face,
            "face_size": list(reversed(face.shape[:2])),
        }

    def recognize_faces(self, current_track_ids):
        comparing_names = list(self.comparing_faces.keys())
        comparing_vectors = np.array(list(self.comparing_faces.values()))

        for track_id in current_track_ids:
            # define face size threshold
            track = self.tracks[track_id]
            appearance = track["appearances"][-1]

            if appearance["face_size"][0] >= self.video_config.recognition_size[0] and \
               appearance["face_size"][1] >= self.video_config.recognition_size[1]:
                if track["identity"] is not None or track["recognition_time"] >= 1:
                    continue

                # get facial vector by face
                facial_vector = face_recognition.predict(appearance["face"])
                track["recognition_time"] += 1

                # compare distances and get the closest vector's index
                distances = np.sqrt(np.square(facial_vector - comparing_vectors).sum(axis=1))
                min_distance = distances.min()

                if min_distance <= self.video_config.recognition_threshold:
                    closest_face_index = distances.argmin()
                    # set name for track
                    track["identity"] = comparing_names[closest_face_index]
            else:
                track["appearances"][-1]["face"] = None
