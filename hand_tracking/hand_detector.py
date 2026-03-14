import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self, max_hands=1, detection_conf=0.8, tracking_conf=0.5):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.results = None

    def detect(self, frame, draw_frame=None):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb)

        if draw_frame is None:
            draw_frame = frame

        self.draw_cached_landmarks(draw_frame)

        return draw_frame

    def draw_cached_landmarks(self, draw_frame):

        if not self.results or not self.results.multi_hand_landmarks:
            return draw_frame

        for hand in self.results.multi_hand_landmarks:

            self.mpDraw.draw_landmarks(
                draw_frame,
                hand,
                self.mpHands.HAND_CONNECTIONS,
                self.mpDraw.DrawingSpec(color=(255, 200, 0), thickness=2, circle_radius=3),
                self.mpDraw.DrawingSpec(color=(0, 255, 255), thickness=2)
            )

        return draw_frame

    def get_landmarks(self, frame):

        lmList = []

        if not self.results or not self.results.multi_hand_landmarks:
            return lmList

        h, w, _ = frame.shape

        hand = self.results.multi_hand_landmarks[0]

        for lm in hand.landmark:

            cx = int(lm.x * w)
            cy = int(lm.y * h)

            lmList.append((cx, cy))

        return lmList

    def fingers_up(self, lmList):

        fingers = [0,0,0,0,0]

        if len(lmList) == 0:
            return fingers

        # thumb
        if lmList[self.tipIds[0]][0] < lmList[self.tipIds[0]-1][0]:
            fingers[0] = 1

        # other fingers
        for i in range(1,5):

            if lmList[self.tipIds[i]][1] < lmList[self.tipIds[i]-2][1]:
                fingers[i] = 1

        return fingers

    def detect_gesture(self, lmList):

        if len(lmList) == 0:
            return "none"

        fingers = self.fingers_up(lmList)

        if all(f == 1 for f in fingers):
            return "erase"

        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            return "draw"

        return "idle"
