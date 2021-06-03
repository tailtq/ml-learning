from image2face import ArcfacePrediction, RetinafacePrediction


face_detection = RetinafacePrediction("mobile0.25", use_cpu=True)
face_recognition = ArcfacePrediction("resnet50", use_cpu=True)
