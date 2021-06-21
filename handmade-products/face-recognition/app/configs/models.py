import os
from image2face import ArcfacePrediction, RetinafacePrediction

import app.utils.pickle_utils as pickle_utils

face_detection = RetinafacePrediction("mobile0.25", use_cpu=True)
face_recognition = ArcfacePrediction("resnet100", use_cpu=True)

pickle_file = "./storage/faces.pickle"
feature_vectors = pickle_utils.load_pickle(pickle_file) if os.path.exists(pickle_file) else {}
