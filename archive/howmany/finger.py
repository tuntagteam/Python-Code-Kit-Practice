import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import mediapipe as mp
import numpy as np
import time

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

def interpret_hand_signal(count):
    """
    Map finger count to gesture label.
    """
    gestures = {
        0: "Fist",
        1: "Point",
        2: "Peace",
        3: "OK",
        4: "Four",
        5: "Open Palm"
    }
    return gestures.get(count, "Unknown")

def draw_glowing_text(img, text, pos, font, scale, color, thickness, glow_color, glow_thickness):
    # Draw glow by drawing the text multiple times with increasing thickness and lower alpha
    overlay = img.copy()
    for i in range(glow_thickness, 0, -1):
        alpha = 0.1 * (glow_thickness - i + 1)
        cv2.putText(overlay, text, pos, font, scale, glow_color, i*2, cv2.LINE_AA)
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    # Draw main text
    cv2.putText(img, text, pos, font, scale, color, thickness, cv2.LINE_AA)

def draw_glowing_circle(img, center, radius, color, glow_color, glow_radius):
    overlay = img.copy()
    for r in range(glow_radius, radius, -1):
        alpha = 0.05 * (glow_radius - r + radius)
        cv2.circle(overlay, center, r, glow_color, thickness=2)
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    cv2.circle(img, center, radius, color, thickness=-1)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        # Create HUD overlay (semi-transparent)
        hud = frame.copy()
        alpha_hud = 0.3
        overlay_color = (10, 30, 40)
        cv2.rectangle(hud, (0,0), (frame.shape[1], 80), overlay_color, -1)
        cv2.addWeighted(hud, alpha_hud, frame, 1 - alpha_hud, 0, frame)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label  # "Left" or "Right"

                # Draw glowing lines and aura around fingers
                landmarks = hand_landmarks.landmark
                h, w, _ = frame.shape

                # Draw connections with glowing effect
                for connection in mp_hands.HAND_CONNECTIONS:
                    start_idx, end_idx = connection
                    start = (int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h))
                    end = (int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h))
                    # Glow line
                    overlay = frame.copy()
                    for thickness in range(6, 2, -1):
                        cv2.line(overlay, start, end, (0, 255, 255), thickness)
                    frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)
                    # Main line
                    cv2.line(frame, start, end, (0, 255, 255), 2)

                # Draw glowing circles (aura) around fingertips
                pulse_radius = 8 + int(4 * abs(np.sin(time.time()*5)))  # Pulsing radius
                for tip_id in tip_ids:
                    cx = int(landmarks[tip_id].x * w)
                    cy = int(landmarks[tip_id].y * h)
                    # Draw aura
                    draw_glowing_circle(frame, (cx, cy), 6, (0, 255, 180), (0, 255, 255), pulse_radius)

                # Count fingers
                count = count_fingers(hand_landmarks, hand_label)
                gesture_label = interpret_hand_signal(count)

                # Draw hand landmarks with a faint glow
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec(color=(0,255,255), thickness=2, circle_radius=3),
                                       mp_draw.DrawingSpec(color=(0,128,128), thickness=1, circle_radius=2))

                # Draw finger count text with sci-fi HUD style
                text_pos = (10, 50) if hand_label == "Right" else (400, 50)
                # Main finger count text
                cv2.putText(
                    frame,
                    f"{hand_label} Hand: {count}",
                    text_pos,
                    cv2.FONT_HERSHEY_DUPLEX,
                    1.2,
                    (0, 255, 255),
                    3,
                    cv2.LINE_AA,
                )
                # Gesture label below count with glowing cyan/teal font and shadow
                gesture_pos = (text_pos[0], text_pos[1] + 40)
                # Shadow
                cv2.putText(frame, gesture_label, (gesture_pos[0]+2, gesture_pos[1]+2),
                            cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 50, 50), 5, cv2.LINE_AA)
                # Glowing text
                draw_glowing_text(frame, gesture_label, gesture_pos, cv2.FONT_HERSHEY_DUPLEX,
                                  1.0, (0, 255, 230), 2, (0, 150, 150), 4)

        cv2.imshow("Finger Counter", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

cap.release()
cv2.destroyAllWindows()