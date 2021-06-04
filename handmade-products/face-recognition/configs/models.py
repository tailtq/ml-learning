import os
from image2face import ArcfacePrediction, RetinafacePrediction

import utils.pickle_utils as pickle_utils

face_detection = RetinafacePrediction("mobile0.25", use_cpu=True)
face_recognition = ArcfacePrediction("resnet50", use_cpu=True)

pickle_file = "../faces.pickle"
feature_vectors = pickle_utils.load_pickle(pickle_file) if os.path.exists(pickle_file) else {}
