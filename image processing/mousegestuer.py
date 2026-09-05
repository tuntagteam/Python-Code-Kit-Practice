"""
HAND MOUSE - Control your computer mouse with hand gestures.

Move the cursor with your index fingertip, click by pinching thumb + index,
double click with two quick pinches.

Press Q or ESC in the camera window to quit.
"""

import math
import sys
import time
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

# =============================================================================
# CONFIGURATION  -  change these values to tune the program
# =============================================================================

# --- Camera -----------------------------------------------------------------
CAMERA_ID = 0            # 0 = default webcam, try 1 or 2 if you have several
CAMERA_WIDTH = 640       # keep this small (640x480 or 1280x720) for speed
CAMERA_HEIGHT = 480
USE_DSHOW = True         # Windows only: DirectShow backend opens the cam faster

# --- Tracking area (the rectangle drawn on the preview) ---------------------
TRACKING_MARGIN = 80     # pixels cut off the left/right camera edges
TRACKING_MARGIN_X = TRACKING_MARGIN
TRACKING_MARGIN_Y = 60   # pixels cut off the top/bottom camera edges

# --- Pinch detection (distance in camera pixels) ----------------------------
PINCH_THRESHOLD = 30     # fingers closer than this  -> pinch STARTS
RELEASE_THRESHOLD = 45   # fingers further than this -> pinch ENDS (hysteresis)

# --- Click timing -----------------------------------------------------------
DOUBLE_PINCH_TIME = 0.35  # seconds allowed between pinch 1 and pinch 2
CLICK_COOLDOWN = 0.20     # minimum seconds between two click events

# --- Cursor movement --------------------------------------------------------
SMOOTHING = 5            # 1 = no smoothing (jittery), 10 = very smooth (laggy)
FREEZE_ON_PINCH = True   # lock the cursor in place during any click gesture
PINCH_ANCHOR_DELAY = 0.15  # seconds of history used to undo pre-pinch drift
EDGE_GUARD = 2           # keeps the cursor off the exact screen corners

# --- Scrolling (thumb + MIDDLE finger pinch) --------------------------------
SCROLL_ENABLED = True
SCROLL_PINCH_THRESHOLD = 30    # thumb-to-middle distance that starts scrolling
SCROLL_RELEASE_THRESHOLD = 45  # ...and the distance that stops it
SCROLL_DEADZONE = 12           # camera pixels of hand movement to ignore
SCROLL_SPEED = 22.0            # scroll steps per second at 100 px of deflection
SCROLL_INVERT = False          # True = hand up scrolls the page down

# --- MediaPipe --------------------------------------------------------------
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
MAX_HANDS = 1
MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")

# --- Interface --------------------------------------------------------------
DEBUG = True             # show distance / state / coordinates on screen
WINDOW_NAME = "Hand Mouse"

# --- MediaPipe landmark numbers ---------------------------------------------
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12

# --- Colours (B, G, R) ------------------------------------------------------
COLOR_MOVE = (0, 220, 0)
COLOR_PINCH = (0, 200, 255)
COLOR_CLICK = (255, 200, 0)
COLOR_DOUBLE = (255, 0, 255)
COLOR_SCROLL = (0, 255, 255)
COLOR_NOHAND = (60, 60, 220)
COLOR_TEXT = (255, 255, 255)
COLOR_BOX = (200, 200, 200)

# =============================================================================
# PyAutoGUI setup
# =============================================================================

pyautogui.FAILSAFE = True   # slam the mouse into a screen corner to abort
pyautogui.PAUSE = 0         # no artificial delay between calls (we need speed)

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_distance(point_a, point_b):
    """Straight line distance in pixels between two (x, y) points."""
    return math.hypot(point_a[0] - point_b[0], point_a[1] - point_b[1])


def map_to_screen(cam_x, cam_y, cam_w, cam_h):
    """
    Convert a point inside the camera tracking rectangle into a real
    monitor coordinate.

    The tracking rectangle (camera pixels) is stretched over the whole screen,
    so a small hand movement covers the entire monitor.
    """
    left = TRACKING_MARGIN_X
    right = cam_w - TRACKING_MARGIN_X
    top = TRACKING_MARGIN_Y
    bottom = cam_h - TRACKING_MARGIN_Y

    # np.interp maps a value from one range onto another range and
    # automatically clamps anything outside the input range.
    screen_x = np.interp(cam_x, (left, right), (0, SCREEN_WIDTH))
    screen_y = np.interp(cam_y, (top, bottom), (0, SCREEN_HEIGHT))

    # Never allow the exact corners, otherwise the PyAutoGUI failsafe fires.
    screen_x = float(np.clip(screen_x, EDGE_GUARD, SCREEN_WIDTH - 1 - EDGE_GUARD))
    screen_y = float(np.clip(screen_y, EDGE_GUARD, SCREEN_HEIGHT - 1 - EDGE_GUARD))
    return screen_x, screen_y


def smooth_position(old_x, old_y, target_x, target_y):
    """
    Exponential smoothing: the cursor walks a fraction of the way toward the
    target every frame instead of teleporting. Higher SMOOTHING = calmer.
    """
    factor = max(1.0, float(SMOOTHING))
    new_x = old_x + (target_x - old_x) / factor
    new_y = old_y + (target_y - old_y) / factor
    return new_x, new_y


def detect_pinch(distance, was_pinched):
    """
    Decide whether the fingers count as pinched, using two thresholds.

    Not pinched yet -> must come closer than PINCH_THRESHOLD to start.
    Already pinched -> stays pinched until it goes past RELEASE_THRESHOLD.

    That gap between the two numbers is the hysteresis that stops shaky
    fingers from flickering between states.
    """
    if was_pinched:
        return distance < RELEASE_THRESHOLD
    return distance < PINCH_THRESHOLD


def detect_scroll_pinch(distance, was_scrolling):
    """Same hysteresis idea as detect_pinch, but for thumb + middle finger."""
    if was_scrolling:
        return distance < SCROLL_RELEASE_THRESHOLD
    return distance < SCROLL_PINCH_THRESHOLD


def handle_scroll(state, scrolling, cam_y, dt):
    """
    Thumb + middle finger pinch = scroll mode.

    The moment the pinch closes we remember the hand's height (the anchor).
    After that the hand works like a joystick: hold it above the anchor to
    scroll up, below it to scroll down. The further from the anchor, the
    faster it scrolls. Letting go stops everything.

    Scroll steps are accumulated as a float so slow movements still produce
    the occasional single step instead of nothing at all.
    """
    if scrolling and not state["scroll_active"]:
        state["scroll_anchor_y"] = cam_y     # first frame of the gesture
        state["scroll_accum"] = 0.0

    if scrolling:
        deflection = state["scroll_anchor_y"] - cam_y      # hand up = positive
        if abs(deflection) > SCROLL_DEADZONE:
            # remove the deadzone so scrolling starts gently, not with a jump
            deflection -= math.copysign(SCROLL_DEADZONE, deflection)
            steps_per_second = (deflection / 100.0) * SCROLL_SPEED
            if SCROLL_INVERT:
                steps_per_second = -steps_per_second
            state["scroll_accum"] += steps_per_second * dt

            whole_steps = int(state["scroll_accum"])
            if whole_steps != 0:
                state["scroll_accum"] -= whole_steps
                pyautogui.scroll(whole_steps)
    else:
        state["scroll_accum"] = 0.0

    state["scroll_active"] = scrolling


def create_state():
    """All the mutable gesture information lives in this one dictionary."""
    return {
        "state": "OPEN",           # OPEN / PINCHED / WAITING_FOR_SECOND_PINCH / SECOND_PINCH
        "pinch_active": False,     # result of detect_pinch on the last frame
        "first_pinch_time": 0.0,   # when the current pinch sequence started
        "last_click_time": 0.0,    # used for the click cooldown
        "last_action": "",         # "CLICK" or "DOUBLE CLICK", for the overlay
        "last_action_time": 0.0,
        "scroll_active": False,    # thumb + middle finger currently pinched
        "scroll_anchor_y": 0.0,    # camera y where the scroll gesture started
        "scroll_accum": 0.0,       # leftover fraction of a scroll step
    }


def process_click(state, pinched, now, hand_visible=True):
    """
    The gesture state machine. Returns "CLICK", "DOUBLE_CLICK" or None.

    Transitions, not raw distance, produce clicks - that is why holding a
    pinch never spams clicks.

        OPEN            --pinch-->   PINCHED
        PINCHED         --release--> WAITING_FOR_SECOND_PINCH  (click is delayed)
        WAITING...      --pinch-->   SECOND_PINCH  + DOUBLE CLICK
        WAITING...      --timeout--> OPEN          + single CLICK
        SECOND_PINCH    --release--> OPEN          (no extra click)

    The single click is deliberately delayed until we know no second pinch is
    coming, so one gesture never fires click + doubleClick together.
    """
    action = None
    current = state["state"]

    # Hand disappeared: abandon an in-progress pinch instead of clicking.
    if not hand_visible and current in ("PINCHED", "SECOND_PINCH"):
        state["state"] = "OPEN"
        return None

    if current == "OPEN":
        if pinched and (now - state["last_click_time"]) > CLICK_COOLDOWN:
            state["state"] = "PINCHED"
            state["first_pinch_time"] = now

    elif current == "PINCHED":
        if not pinched:
            if now - state["first_pinch_time"] > DOUBLE_PINCH_TIME:
                # Held too long to be half of a double pinch -> click now.
                action = "CLICK"
                state["state"] = "OPEN"
            else:
                # Quick pinch: wait a moment to see if a second one arrives.
                state["state"] = "WAITING_FOR_SECOND_PINCH"

    elif current == "WAITING_FOR_SECOND_PINCH":
        if pinched:
            action = "DOUBLE_CLICK"
            state["state"] = "SECOND_PINCH"
        elif now - state["first_pinch_time"] > DOUBLE_PINCH_TIME:
            action = "CLICK"
            state["state"] = "OPEN"

    elif current == "SECOND_PINCH":
        if not pinched:
            state["state"] = "OPEN"

    if action is not None:
        state["last_click_time"] = now
        state["last_action"] = "CLICK" if action == "CLICK" else "DOUBLE CLICK"
        state["last_action_time"] = now

    return action


def current_gesture(state, hand_visible, now):
    """Human readable gesture label plus a colour, for the overlay."""
    if now - state["last_action_time"] < 0.45 and state["last_action"]:
        if state["last_action"] == "DOUBLE CLICK":
            return "DOUBLE CLICK", COLOR_DOUBLE
        return "CLICK", COLOR_CLICK
    if not hand_visible:
        return "NO HAND", COLOR_NOHAND
    if state["scroll_active"]:
        return "SCROLL", COLOR_SCROLL
    if state["pinch_active"]:
        return "PINCH", COLOR_PINCH
    return "MOVE", COLOR_MOVE


def draw_interface(frame, info):
    """Draw the tracking box, the fingertips and the text panel."""
    h, w = frame.shape[:2]

    # --- tracking rectangle -------------------------------------------------
    cv2.rectangle(
        frame,
        (TRACKING_MARGIN_X, TRACKING_MARGIN_Y),
        (w - TRACKING_MARGIN_X, h - TRACKING_MARGIN_Y),
        COLOR_BOX, 2,
    )
    cv2.putText(frame, "tracking area", (TRACKING_MARGIN_X, TRACKING_MARGIN_Y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_BOX, 1)

    # --- fingertips ---------------------------------------------------------
    if info["hand_visible"]:
        ix, iy = info["index_px"]
        tx, ty = info["thumb_px"]
        cx, cy = info["middle_px"]
        line_color = info["color"]
        cv2.line(frame, (tx, ty), (ix, iy), line_color, 2)
        cv2.circle(frame, (ix, iy), 12, info["color"], cv2.FILLED)   # index tip
        cv2.circle(frame, (ix, iy), 16, (255, 255, 255), 2)
        cv2.circle(frame, (tx, ty), 9, (0, 165, 255), cv2.FILLED)    # thumb tip
        cv2.circle(frame, (cx, cy), 7, COLOR_SCROLL, cv2.FILLED)     # middle tip

        # midpoint distance readout
        mx, my = (ix + tx) // 2, (iy + ty) // 2
        cv2.putText(frame, f"{info['distance']:.0f}", (mx + 8, my - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # while scrolling, show the anchor height and the current deflection
        if info["scroll_active"]:
            anchor_y = int(info["scroll_anchor_y"])
            cv2.line(frame, (0, anchor_y), (w, anchor_y), COLOR_SCROLL, 1)
            cv2.line(frame, (cx, anchor_y), (cx, cy), COLOR_SCROLL, 3)
            cv2.putText(frame, "SCROLL", (cx + 14, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_SCROLL, 2)

    # --- status panel -------------------------------------------------------
    lines = [
        ("HAND MOUSE", COLOR_TEXT),
        (f"Gesture: {info['gesture']}", info["color"]),
        (f"Pinch:   {'CLOSED' if info['pinch_active'] else 'OPEN'}", COLOR_TEXT),
        (f"Mouse:   {int(info['screen_x'])}, {int(info['screen_y'])}", COLOR_TEXT),
        (f"FPS:     {info['fps']:.0f}", COLOR_TEXT),
    ]

    if DEBUG:
        lines += [
            ("-- debug --", COLOR_BOX),
            (f"Distance: {info['distance']:.1f} / {PINCH_THRESHOLD}", COLOR_BOX),
            (f"Scroll d: {info['scroll_distance']:.1f} / {SCROLL_PINCH_THRESHOLD}", COLOR_BOX),
            (f"State:    {info['state']}", COLOR_BOX),
            (f"Camera:   {info['index_px'][0]}, {info['index_px'][1]}", COLOR_BOX),
            (f"Screen:   {int(info['screen_x'])}, {int(info['screen_y'])}", COLOR_BOX),
        ]

    panel_h = 22 * len(lines) + 14
    overlay = frame.copy()
    cv2.rectangle(overlay, (8, 8), (250, 8 + panel_h), (0, 0, 0), cv2.FILLED)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    y = 30
    for text, color in lines:
        cv2.putText(frame, text, (18, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1)
        y += 22

    # small hint at the bottom
    cv2.putText(frame, "Q / ESC = quit", (10, h - 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_BOX, 1)
    return frame


def open_camera():
    """Open the webcam and set the requested resolution."""
    if USE_DSHOW and sys.platform.startswith("win"):
        cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(CAMERA_ID)

    if not cap.isOpened():                      # fall back to the default backend
        cap = cv2.VideoCapture(CAMERA_ID)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    return cap


# =============================================================================
# MAIN LOOP
# =============================================================================

def main():
    print(f"Screen resolution detected: {SCREEN_WIDTH} x {SCREEN_HEIGHT}")
    print("Starting webcam... press Q or ESC in the window to quit.")

    if not MODEL_PATH.is_file():
        print(f"ERROR: MediaPipe model not found: {MODEL_PATH}")
        return

    cap = open_camera()
    if not cap.isOpened():
        print(f"ERROR: could not open camera {CAMERA_ID}. "
              f"Close other apps using the webcam or try CAMERA_ID = 1.")
        return

    options = vision.HandLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=MAX_HANDS,
        min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_hand_presence_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    )
    hands = vision.HandLandmarker.create_from_options(options)

    state = create_state()

    # Cursor position we are smoothing toward; start where the mouse is now.
    cursor_x, cursor_y = pyautogui.position()
    cursor_x, cursor_y = float(cursor_x), float(cursor_y)

    # free_x/free_y follow the finger every frame; cursor_x/cursor_y is what we
    # actually send to the mouse (identical, unless a gesture has frozen it).
    free_x, free_y = cursor_x, cursor_y
    frozen_pos = None
    history = []                 # recent (time, x, y) samples for the rewind
    had_hand_last_frame = False

    fps = 0.0
    prev_time = time.time()
    last_frame_timestamp_ms = -1

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("WARNING: dropped a camera frame.")
                continue

            # Mirror the image so moving right moves the cursor right.
            frame = cv2.flip(frame, 1)
            cam_h, cam_w = frame.shape[:2]

            # MediaPipe wants RGB; OpenCV gives BGR.
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            frame_timestamp_ms = max(
                last_frame_timestamp_ms + 1,
                time.monotonic_ns() // 1_000_000,
            )
            last_frame_timestamp_ms = frame_timestamp_ms
            results = hands.detect_for_video(mp_image, frame_timestamp_ms)

            now = time.time()
            hand_visible = False
            index_px = (0, 0)
            thumb_px = (0, 0)
            middle_px = (0, 0)
            distance = 999.0
            scroll_distance = 999.0

            if results.hand_landmarks:
                hand = results.hand_landmarks[0]
                lm = hand

                index = lm[INDEX_TIP]
                thumb = lm[THUMB_TIP]
                middle = lm[MIDDLE_TIP]

                # Landmarks are normalised 0..1; anything far outside means the
                # fingertip is off-frame and should not be trusted.
                if -0.05 <= index.x <= 1.05 and -0.05 <= index.y <= 1.05:
                    hand_visible = True
                    index_px = (int(index.x * cam_w), int(index.y * cam_h))
                    thumb_px = (int(thumb.x * cam_w), int(thumb.y * cam_h))
                    middle_px = (int(middle.x * cam_w), int(middle.y * cam_h))
                    distance = calculate_distance(index_px, thumb_px)
                    scroll_distance = calculate_distance(middle_px, thumb_px)

                vision.drawing_utils.draw_landmarks(
                    frame,
                    hand,
                    vision.HandLandmarksConnections.HAND_CONNECTIONS,
                    vision.drawing_styles.get_default_hand_landmarks_style(),
                    vision.drawing_styles.get_default_hand_connections_style(),
                )

            dt = max(1e-3, now - prev_time)

            # --- scroll gesture (checked first, it overrides clicking) --------
            scrolling = False
            if SCROLL_ENABLED and hand_visible:
                scrolling = detect_scroll_pinch(scroll_distance, state["scroll_active"])
            handle_scroll(state, scrolling, middle_px[1], dt)

            # --- click gesture -------------------------------------------------
            # While scrolling we force the click machine back to OPEN so the
            # two gestures can never fire at the same time.
            if hand_visible and not state["scroll_active"]:
                state["pinch_active"] = detect_pinch(distance, state["pinch_active"])
            else:
                state["pinch_active"] = False

            clicks_allowed = hand_visible and not state["scroll_active"]
            action = process_click(state, state["pinch_active"], now, clicks_allowed)

            # --- cursor movement ---------------------------------------------
            if hand_visible:
                target_x, target_y = map_to_screen(index_px[0], index_px[1], cam_w, cam_h)

                if not had_hand_last_frame:
                    # Just re-acquired the hand: jump straight to the finger
                    # instead of sliding across the screen from the old spot.
                    free_x, free_y = target_x, target_y
                else:
                    free_x, free_y = smooth_position(free_x, free_y, target_x, target_y)

                # Keep a short history of where the cursor was, so we can rewind.
                history.append((now, free_x, free_y))
                while len(history) > 1 and now - history[0][0] > PINCH_ANCHOR_DELAY:
                    history.pop(0)

                # Any gesture in progress = the cursor must stand still. That
                # includes WAITING_FOR_SECOND_PINCH, so the cursor does not
                # wander between the two pinches of a double click.
                gesture_busy = (state["scroll_active"]
                                or state["pinch_active"]
                                or state["state"] != "OPEN")

                if FREEZE_ON_PINCH and gesture_busy:
                    if frozen_pos is None:
                        # Rewind to where the cursor was BEFORE the fingers
                        # started closing - that pre-pinch drift is exactly
                        # what makes clicks land in the wrong place.
                        frozen_pos = (history[0][1], history[0][2])
                    cursor_x, cursor_y = frozen_pos
                else:
                    if frozen_pos is not None:
                        # Gesture finished: glide back from the frozen point.
                        free_x, free_y = frozen_pos
                        frozen_pos = None
                        history.clear()
                    cursor_x, cursor_y = free_x, free_y

                pyautogui.moveTo(int(cursor_x), int(cursor_y), _pause=False)
            # If the hand is lost we simply do nothing: the cursor stays put.

            had_hand_last_frame = hand_visible

            # --- real mouse actions -------------------------------------------
            if action == "CLICK":
                pyautogui.click()
            elif action == "DOUBLE_CLICK":
                pyautogui.doubleClick()

            # --- FPS ----------------------------------------------------------
            frame_time = now - prev_time
            prev_time = now
            if frame_time > 0:
                fps = 0.9 * fps + 0.1 * (1.0 / frame_time) if fps else 1.0 / frame_time

            # --- draw ----------------------------------------------------------
            gesture, color = current_gesture(state, hand_visible, now)
            draw_interface(frame, {
                "hand_visible": hand_visible,
                "index_px": index_px,
                "thumb_px": thumb_px,
                "middle_px": middle_px,
                "distance": distance if hand_visible else 0.0,
                "scroll_distance": scroll_distance if hand_visible else 0.0,
                "scroll_active": state["scroll_active"],
                "scroll_anchor_y": state["scroll_anchor_y"],
                "pinch_active": state["pinch_active"],
                "state": state["state"],
                "gesture": gesture,
                "color": color,
                "screen_x": cursor_x,
                "screen_y": cursor_y,
                "fps": fps,
            })

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q') or key == 27:   # 27 = ESC
                break
            # Also quit if the user closes the window with the X button.
            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

    except pyautogui.FailSafeException:
        print("PyAutoGUI failsafe triggered (mouse hit a screen corner). Exiting.")
    except KeyboardInterrupt:
        print("Stopped with Ctrl+C.")
    except Exception as error:                  # keep the camera from staying locked
        print(f"ERROR: {error}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        try:
            hands.close()
        except Exception:
            pass
        print("Camera released. Bye!")


if __name__ == "__main__":
    main()
