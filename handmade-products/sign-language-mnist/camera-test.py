import cv2
import time
import pickle
import imutils
import matplotlib.pyplot as plt
from imutils.video import VideoStream
from tensorflow.keras.models import load_model

vs = VideoStream(src=0, framerate=6).start()
model = load_model('basic_model.h5')

# load OneHotEncoder
file = open('sign-language.obj', 'rb')
encoder = pickle.load(file)
file.close()

characters = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    10: 'K',
    11: 'L',
    12: 'M',
    13: 'N',
    14: 'O',
    15: 'P',
    16: 'Q',
    17: 'R',
    18: 'S',
    19: 'T',
    20: 'U',
    21: 'V',
    22: 'W',
    23: 'X',
    24: 'Y',
}

time.sleep(1.0)

cv2.imshow('Language', cv2.imread('sign.png'))

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    frame_shape = frame.shape

    image = frame[:175, frame_shape[1] - 175:frame_shape[1] - 1]
    image = cv2.flip(image, 1)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = gray
    gray = cv2.resize(gray, (28, 28))
    gray = gray / 255.0

    prediction = model.predict(gray.reshape(1, 28, 28, 1))
    result = encoder.inverse_transform(prediction)
    result_text = characters[result[0][0]]
    # if result[0][0] != 24:
    #     result_text = characters[result[0][0]]
    # else:
    #     print(result)
    #     result_text = ''
    # frame = imutils.resize(frame, width=450)
    frame_shape = frame.shape

    cv2.rectangle(frame, (frame_shape[1], 0), (frame_shape[1] - 175, 175), color=(0, 0, 255), thickness=1)
    cv2.putText(frame, result_text, (0, 100),
                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=3,
                color=(0, 255, 0),
                thickness=2)
    cv2.imshow('My hand', image)
    cv2.imshow('Me', frame)
    # cv2.waitKey(0)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

vs.stop()
cv2.destroyAllWindows()
