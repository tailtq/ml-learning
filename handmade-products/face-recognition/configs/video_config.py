class VideoConfig:
    def __init__(self,
                 drop_last_frame_in_n_steps=0,
                 detection_size=(480, -1),
                 recognition_size=(112, 112)):
        # for dropping frame, drop_last_frame_in_n_steps value should be in [2, n] range
        self.drop_last_frame_in_n_steps = drop_last_frame_in_n_steps
        self.detection_size = detection_size
        self.recognition_size = recognition_size


class ProcessStatus:
    def __init__(self,
                 image_decoding_status=False,
                 detecting_status=False,
                 tracking_status=False):
        self.image_decoding_status = image_decoding_status
        self.detecting_status = detecting_status
        self.tracking_status = tracking_status
