import cv2


def draw_tracks(frame, tracks):
    frame = frame.copy()

    for track in tracks:
        coordinates = [int(i) for i in track[:4]]
        x1y1, x2y2 = (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3])
        cv2.rectangle(frame, x1y1, x2y2, (0, 255, 0))

        cv2.putText(frame, str(track[4]), x1y1, cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 2)

    return frame
