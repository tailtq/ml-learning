import queue
from datetime import datetime

from app.services.attendance_service import AttendanceDBPersistence
from app.utils.local_storage_utils import LocalStorageUtils
from sort.sort import *
from app.configs.models import face_recognition, face_detection
from app.configs.video_config import VideoConfig, ProcessStatus
from app.threads.base_thread import BaseThread


class TrackingThread(BaseThread):
    def __init__(self,
                 comparing_vectors,
                 comparing_person_ids,
                 video_config: VideoConfig,
                 process_status: ProcessStatus,
                 tracking_queue: queue.Queue,
                 visualization_queue: queue.Queue):
        super().__init__()

        self.comparing_vectors = comparing_vectors
        self.comparing_person_ids = comparing_person_ids
        self.video_config = video_config
        self.process_status = process_status
        self.tracking_queue = tracking_queue
        self.visualization_queue = visualization_queue
        self.tracker = Sort()
        self.tracks = {}
        self.attendance_db_persistence = AttendanceDBPersistence()

    def _run(self):
        """
        Run the stream and push each frame into a queue
        :return:
        """
        print(f"TrackingThread is running")

        start_time = time.time()

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
                        "appeared_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "track_id": track_id,
                        "person_id": None,
                        "recognition_time": 0,
                        "appearances": [],
                        "inserted": False
                    }

                self.tracks[track_id]["appearances"].append(self._convert_track_format(track, frame, frame_index))

            # apply face recognition
            current_tracks = self.recognize_faces(current_track_ids)

            for current_track in current_tracks:
                if current_track["person_id"] is not None and \
                     not current_track["inserted"] and \
                     not self.attendance_db_persistence.is_attended_today(current_track["person_id"]):

                    avatar_path = LocalStorageUtils.save_image(current_track["appearances"][-1]["face"],
                                                               self.video_config.face_storage_path)

                    self.attendance_db_persistence.create({
                        "person_id": current_track["person_id"],
                        "avatar": avatar_path,
                        "confidence": 0,
                        "attended_at": current_track["appeared_at"],
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    current_track["inserted"] = True

            # self.visualization_queue.put({
            #     "tracks": current_tracks,
            #     "frame": frame,
            #     "frame_index": frame_index,
            # })

        print(f"{self.__class__.__name__}: {time.time() - start_time}")

        self.process_status.tracking_status = True

    @staticmethod
    def _convert_track_format(track, frame, frame_index):
        """
        Get new format for inserting to SORT algorithm
        :param track:
        :return: tuple
        """
        track[track < 0] = 0.
        face = face_detection.align_face(frame, np.concatenate((track[:4], track[5:])))

        return {
            "frame_index": frame_index,
            "box": [track[0], track[1], track[2], track[3]],
            "confidence": track[5],
            "face": face,
            "face_size": list(reversed(face.shape[:2])),
        }

    def recognize_faces(self, current_track_ids):
        for track_id in current_track_ids:
            # define face size threshold
            track = self.tracks[track_id]
            appearance = track["appearances"][-1]

            if appearance["face_size"][0] >= self.video_config.recognition_size[0] and \
               appearance["face_size"][1] >= self.video_config.recognition_size[1]:
                if track["person_id"] is not None or track["recognition_time"] >= 1:
                    continue

                # get facial vector by face
                facial_vector = face_recognition.predict(appearance["face"])
                track["recognition_time"] += 1

                # compare distances and get the closest vector's index
                distances = np.sqrt(np.square(facial_vector - self.comparing_vectors).sum(axis=1))
                min_distance = distances.min()
                print(f"Min distance: {min_distance}")

                if min_distance <= self.video_config.recognition_threshold:
                    closest_face_index = distances.argmin()
                    # set name for track
                    track["person_id"] = self.comparing_person_ids[closest_face_index]
            else:
                track["appearances"][-1]["face"] = None

        return [self.tracks[track_id] for track_id in current_track_ids]
