# pip install mediapipe opencv-python

import cv2
#import mediapipe as mp
#mp_face_detection = mp.solutions.face_detection
#mp_drawing = mp.solutions.drawing_utils
#mp_holistic = mp.solutions.holistic

# For webcam input:
cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024) # 크기 제한이 있는 것 같다.
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768) # 크기 제한이 있는 것 같다.

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      print("Ignoring empty camera frame.")
      continue

    # frame.shape (세로, 가로, 색)
    h = frame.shape[0]
    w = frame.shape[1]

    result = frame.copy()
    src = frame.copy()
    result[0:h, 0:w//2] = frame[0:h, 0:w//2]
    result[0:h, w//2:w] = cv2.flip(frame[0:h, 0:w//2], 1)

    cv2.imshow('', result)

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()
