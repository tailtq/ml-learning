import os
import numpy as np
import utils.pickle_utils as pickle_utils
from image2face import ArcfacePrediction, RetinafacePrediction

face_detection = RetinafacePrediction("mobile0.25", use_cpu=True)
face_recognition = ArcfacePrediction("resnet100", use_cpu=True)

pickle_file = "./faces.pickle"
feature_vectors = pickle_utils.load_pickle(pickle_file) if os.path.exists(pickle_file) else {}

CONFIG = {
    "DROP_FRAME_AFTER_STEP": 2,
    "THRESHOLD": 0.1,
    "FACES": {
        "VECTORS": np.array(list(feature_vectors.values())),
        "NAMES": list(feature_vectors.keys())
    }
}

assert CONFIG["DROP_FRAME_AFTER_STEP"] != 0 and CONFIG["DROP_FRAME_AFTER_STEP"] != 1
