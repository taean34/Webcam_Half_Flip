# pip install opencv-python
import cv2

# For webcam input:
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    # frame.shape (세로, 가로, 색 채널)
    h = frame.shape[0]
    w = frame.shape[1]
    
    # 대칭
    flip = cv2.flip(frame, 1)
    
    # 일부분만 대칭
    fliphalf = frame.copy()
    fliphalf[0:h, w//2:w] = cv2.flip(fliphalf[0:h, 0:w//2], 1)

    # 보여주기
    cv2.imshow('original', frame)
    cv2.imshow('flip', flip)
    cv2.imshow('fliphalf', fliphalf)
    
    # [ESC]키를 누르면 종료
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()
