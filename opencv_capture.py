# pip install opencv-python
import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():  # 계속 반복
    ret, frame = cap.read()  # 프레임(장면) 1개 로딩
    h = frame.shape[0]       # 높이(세로길이)
    w = frame.shape[1]       # 너비(가로길)
    
    # 원본
    original = frame.copy()
    
    
    # 결과 보여주기
    cv2.imshow('original', original)
    
    # [ESC]키를 누르면 종료
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()
