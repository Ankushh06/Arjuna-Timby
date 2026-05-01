import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import Angles
import cvzone
import serial

# Camera setup
camera = cv2.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

# Serial communication
serialcomm = serial.Serial('COM6', 115200)
time.sleep(2)

# Hand detector
detector = HandDetector(detectionCon=0.4, maxHands=1)

# Polynomial coefficients (Z distance)
A = 0.012636680507237852
B = -2.710541724316941
C = 182.62076069382988

# Screen center
scrnCenter_x = 640
scrnCenter_y = 360

# Smoothing variables
prevX, prevY = 90, 90
alpha = 0.15    #0.2 tha

# Laser blinking
lastBlink = 0

while True:
    success, img = camera.read()
    hands, img = detector.findHands(img, draw=False)

    # ================= HAND DETECTION =================
    if hands:
        serialcomm.write("%H1#".encode())  # hand detected

        hand = hands[0]
        lmList = hand['lmList']
        bx, by, bw, bh = hand['bbox']

        # Gesture detection
        fingers = detector.fingersUp(hand)

        # Draw box
        cvzone.cornerRect(img, (bx, by, bw, bh), l=20, t=3)

        # Landmark points
        hand_x1, hand_y1, _ = lmList[5]
        hand_x2, hand_y2, _ = lmList[17]

        center_x = (hand_x1 + hand_x2) / 2
        center_y = (hand_y1 + hand_y2) / 2

        cx, cy = int(center_x), int(center_y)

        # Crosshair
        cv2.line(img, (cx - 15, cy), (cx + 15, cy), (0, 0, 255), 2)
        cv2.line(img, (cx, cy - 15), (cx, cy + 15), (0, 0, 255), 2)

        distance_virtual = ((hand_x2-hand_x1)**2 + (hand_y2-hand_y1)**2)**0.5

        # Z calculation
        if distance_virtual > 153:
            Z_real = (-0.125 * distance_virtual) + 44.125
        elif distance_virtual > 107:
            Z_real = (-0.217391304348 * distance_virtual) + 58.2608695652
        else:
            Z_real = (A * (distance_virtual**2)) + (B * distance_virtual) + C

        # X, Y calculation (mirrored X)
        X_virtual = (center_x - scrnCenter_x)
        Y_virtual = -(center_y - scrnCenter_y)

        X_real = X_virtual * (6.3 / distance_virtual)
        Y_real = Y_virtual * (6.3 / distance_virtual)

        # Angles
        angles = Angles.turret(X_real, Y_real, Z_real)
        angles.offsets(12, 0, 7)
        angles.getAngles()

        newX = int(angles.getTheta_x()) + 10
        newY = int(angles.getTheta_y()) + 3

        # Smoothing
        smoothX = int(prevX + alpha * (newX - prevX))
        smoothY = int(prevY + alpha * (newY - prevY))
        prevX, prevY = smoothX, smoothY

        # Limit angles
        smoothX = max(0, min(180, smoothX))
        smoothY = max(0, min(180, smoothY))

        # ================= GESTURE CONTROL =================

        if fingers == [0,0,0,0,0]:   # ✊ CLOSED → MOVE
            move = True
            laser = False

        elif fingers == [1,1,1,1,1]: # ✋ OPEN → BLINK
            move = False
            laser = True

        else:
            move = False
            laser = False

        # ================= SERIAL =================

        # Movement
        if move:
            motorX = "%" + "X" + str(smoothX) + "#"
            motorY = "%" + "Y" + str(smoothY) + "#"

            serialcomm.write(motorX.encode())
            serialcomm.write(motorY.encode())

        # Laser blinking
        currentTime = time.time()

        if laser:
            serialcomm.write("%L1#".encode())  # blink mode
        else:
            serialcomm.write("%L0#".encode())

        # ================= UI =================

        label_y = by - 10 if by > 40 else by + bh + 30

        cv2.rectangle(img, (bx, label_y - 20), (bx + 180, label_y + 5), (0,0,0), -1)

        cv2.putText(img, "TARGET LOCKED", (bx, label_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        info_y = by + bh + 25
        cv2.putText(img, f"X: {smoothX}", (bx, info_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        cv2.putText(img, f"Y: {smoothY}", (bx, info_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # Mode display
        if move:
            cv2.putText(img, "MOVE MODE", (50,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        if laser:
            cv2.putText(img, "FIRE MODE", (50,150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # Debug
        print(f"X: {smoothX}, Y: {smoothY}")

        cv2.putText(img, f'X:{smoothX} Y:{smoothY}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # ================= NO HAND =================
    else:
        serialcomm.write("%H0#".encode())  # no hand

    cv2.imshow("Turret Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()