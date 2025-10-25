import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Finger tip landmark IDs
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks, hand_label):
    """
    Count raised fingers for a single hand.
    Adjusts thumb logic for left/right hands.
    """
    count = 0
    landmarks = hand_landmarks.landmark

    # Thumb logic depends on hand orientation
    if hand_label == "Right":
        if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x:
            count += 1
    else:  # Left hand
        if landmarks[tip_ids[0]].x > landmarks[tip_ids[0] - 1].x:
            count += 1

    # Other fingers (index to pinky)
    for i in range(1, 5):
        if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:
            count += 1

    return count

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label  # "Left" or "Right"

                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Count fingers
                count = count_fingers(hand_landmarks, hand_label)

                # Draw result
                text_pos = (10, 50) if hand_label == "Right" else (400, 50)
                cv2.putText(
                    frame,
                    f"{hand_label} Hand: {count}",
                    text_pos,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                )

        cv2.imshow("Finger Counter", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

cap.release()
cv2.destroyAllWindows()