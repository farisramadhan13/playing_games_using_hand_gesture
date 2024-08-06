import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey
from directkeys import UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW
import time

detector = HandDetector(detectionCon=0.8, maxHands=2)

time.sleep(2.0)
current_key_pressed = set()

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Flip the frame horizontally to create a mirror effect
    frame = cv2.flip(frame, 1)

    keyPressed = False
    hands, img = detector.findHands(frame)
    
    # Note: Update rectangle coordinates to fit the mirrored image
    cv2.rectangle(img, (0, 480), (300, 425), (59, 11, 94), -2)
    cv2.rectangle(img, (640, 480), (340, 425), (59, 11, 94), -2)
    
    if hands:
        for hand in hands:
            lmList = hand
            fingerUp = detector.fingersUp(lmList)
            if hand['type'] == 'Left':
                if fingerUp == [1, 1, 1, 1, 1]:
                    cv2.putText(frame, 'Right', (360, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                    PressKey(RIGHT_ARROW)
                    current_key_pressed.add(RIGHT_ARROW)
                    keyPressed = True
                elif fingerUp == [0, 1, 0, 0, 0]:
                    cv2.putText(frame, 'Up', (360, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                    PressKey(UP_ARROW)
                    current_key_pressed.add(UP_ARROW)
                    keyPressed = True
            elif hand['type'] == 'Right':
                if fingerUp == [1, 1, 1, 1, 1]:
                    cv2.putText(frame, 'Left', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                    PressKey(LEFT_ARROW)
                    current_key_pressed.add(LEFT_ARROW)
                    keyPressed = True
                elif fingerUp == [0, 1, 0, 0, 0]:
                    cv2.putText(frame, 'Down', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
                    PressKey(DOWN_ARROW)
                    current_key_pressed.add(DOWN_ARROW)
                    keyPressed = True

        if not keyPressed and len(current_key_pressed) != 0:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed = set()
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
