import cv2
import mediapipe as mp
from math import sqrt

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(model_complexity=0)
mpDraw = mp.solutions.drawing_utils

grabs = {}

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if not success:
        print('fuck')
        exit()

    # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for i in range(len(results.multi_hand_landmarks)): # working with each hand
            handLms = results.multi_hand_landmarks[i]
            fingertips = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
    
                if id != 0 and id%4 == 0:
                    cv2.circle(image, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    cv2.putText(image, str(i) + str(id//4-1), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))
                    fingertips.append((int(lm.x*w), int(lm.y*h)))

            #print(fingertips)
            for j in range(len(fingertips)):
                for k in range(j, len(fingertips)):
                    cv2.line(image, fingertips[i], fingertips[j], (255, 255, 0))

            grab_point = (
                int((fingertips[0][0]+fingertips[1][0])/2),
                int((fingertips[0][1]+fingertips[1][1])/2)
            )
            thumb_index_distance = sqrt((fingertips[0][0]-fingertips[1][0])**2 + (fingertips[0][1]-fingertips[1][1])**2)
            if thumb_index_distance <= 100:
                if not i in grabs:
                    grabs[i] = {'point': grab_point, 'frames': 0, 'fingers_closeness': int(thumb_index_distance)}
                else:
                    grabs[i] = {'point': grab_point, 'frames': grabs[i]['frames']+1, 'fingers_closeness': int(thumb_index_distance)}
            else:
                if i in grabs:
                    del grabs[i]

        print(grabs)
        for grab_id in grabs:
            grab = grabs[grab_id]
            cv2.circle(image, grab['point'], int(grab['fingers_closeness']), (128, 0, 255), 5)
            cv2.putText(image, str(grab['frames']), grab['point'], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 128))

        #mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", image)
    cv2.waitKey(1)