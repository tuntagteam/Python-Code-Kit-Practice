import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Tip IDs for fingers (thumb, index, middle, ring, pinky)
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    """
    Given landmarks of one hand, returns number of raised fingers.
    Very simple logic: compare x/y of tip vs some reference joint.
    """
    count = 0
    # For thumb, compare x-coordinate (for right hand) or reverse for left hand
    # This example is for one hand (e.g. right hand)
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 2].x:
        count += 1
    # For other four fingers: compare y-coordinate of tip vs the PIP joint (two indices behind)
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            count += 1
    return count

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Flip horizontally for mirror view
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                count = count_fingers(hand_landmarks)
                cv2.putText(frame, f"Fingers: {count}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Finger Counter", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # press ESC to quit
            break

cap.release()
cv2.destroyAllWindows()