"""A polished real-time hand gesture recognition studio.

Controls: Q/Esc quit, Space pause, S screenshot, L landmarks, H dashboard, M mirror.
"""

from __future__ import annotations

import argparse
import os
import tempfile
import time
import urllib.request
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


APP_NAME = "Nanon Gesture Studio"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
)
SCRIPT_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = SCRIPT_DIR / "captures"

# BGR colors used throughout the interface.
INK = (244, 247, 255)
MUTED = (166, 174, 194)
PANEL = (19, 23, 36)
CYAN = (255, 204, 72)
PURPLE = (225, 105, 178)
GREEN = (128, 224, 113)

# MediaPipe's 21-point hand topology. Keeping it local works with both the
# classic ``mediapipe.solutions`` package and newer Tasks-only releases.
HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
)


@dataclass
class HandReading:
    """The display-ready result for one detected hand."""

    side: str
    gesture: str
    confidence: float
    landmarks: list


class GestureSmoother:
    """Stabilize noisy frame-by-frame predictions with a short vote window."""

    def __init__(self, window_size: int = 7) -> None:
        self.window_size = window_size
        self.history: dict[str, deque[tuple[str, float]]] = {}

    def update(self, hand_key: str, gesture: str, confidence: float) -> tuple[str, float]:
        samples = self.history.setdefault(hand_key, deque(maxlen=self.window_size))
        samples.append((gesture, confidence))
        counts = Counter(label for label, _ in samples)
        scores = {
            label: sum(score for name, score in samples if name == label)
            for label in counts
        }
        stable = max(counts, key=lambda label: (counts[label], scores[label]))
        matching = [score for label, score in samples if label == stable]
        return stable, sum(matching) / len(matching)

    def clear(self) -> None:
        self.history.clear()


class FpsMeter:
    def __init__(self, window_size: int = 24) -> None:
        self.samples: deque[float] = deque(maxlen=window_size)
        self.last_time = time.perf_counter()

    def tick(self) -> float:
        now = time.perf_counter()
        elapsed = now - self.last_time
        self.last_time = now
        if elapsed > 0:
            self.samples.append(1.0 / elapsed)
        return sum(self.samples) / len(self.samples) if self.samples else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--camera", type=int, default=0, help="camera device index")
    parser.add_argument("--confidence", type=float, default=0.55, help="minimum gesture score")
    parser.add_argument("--hands", type=int, default=2, choices=(1, 2), help="hands to track")
    parser.add_argument("--width", type=int, default=1280, help="camera capture width")
    parser.add_argument("--height", type=int, default=720, help="camera capture height")
    parser.add_argument("--model", type=Path, help="path to a gesture_recognizer.task model")
    return parser.parse_args()


def model_path_from(args: argparse.Namespace) -> Path:
    if args.model:
        return args.model.expanduser().resolve()

    # Support launching from either the repository root or NanonProject itself.
    candidates = (
        SCRIPT_DIR / "gesture_recognizer.task",
        SCRIPT_DIR.parent / "gesture_recognizer.task",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def ensure_model(model_path: Path) -> None:
    if model_path.exists():
        return

    model_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Model not found. Downloading to {model_path} ...")
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, dir=model_path.parent, suffix=".download"
        ) as temp:
            temp_path = Path(temp.name)
        urllib.request.urlretrieve(MODEL_URL, temp_path)
        temp_path.replace(model_path)
        print("Model ready.")
    except Exception as error:
        if temp_path and temp_path.exists():
            temp_path.unlink()
        raise RuntimeError(
            f"Could not download the gesture model. Download it manually from\n"
            f"{MODEL_URL}\nand save it as {model_path}"
        ) from error


def rounded_rect(
    image: np.ndarray,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    radius: int = 18,
    thickness: int = -1,
) -> None:
    """Draw a rounded rectangle using only OpenCV primitives."""
    x1, y1 = start
    x2, y2 = end
    radius = max(1, min(radius, (x2 - x1) // 2, (y2 - y1) // 2))
    if thickness < 0:
        cv2.rectangle(image, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(image, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        for center in (
            (x1 + radius, y1 + radius),
            (x2 - radius, y1 + radius),
            (x1 + radius, y2 - radius),
            (x2 - radius, y2 - radius),
        ):
            cv2.circle(image, center, radius, color, -1)
    else:
        cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
        cv2.ellipse(image, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(image, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(image, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)
        cv2.ellipse(image, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)


def glass_panel(
    image: np.ndarray,
    start: tuple[int, int],
    end: tuple[int, int],
    alpha: float = 0.82,
) -> None:
    overlay = image.copy()
    rounded_rect(overlay, start, end, PANEL, 20)
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)


def label(
    image: np.ndarray,
    text: str,
    position: tuple[int, int],
    scale: float = 0.55,
    color: tuple[int, int, int] = INK,
    thickness: int = 1,
) -> None:
    cv2.putText(
        image, text, position, cv2.FONT_HERSHEY_SIMPLEX,
        scale, color, thickness, cv2.LINE_AA
    )


def title_case_gesture(name: str) -> str:
    return name.replace("_", " ").strip().title() if name else "No Gesture"


def draw_hand(
    image: np.ndarray,
    reading: HandReading,
    hand_index: int,
    show_landmarks: bool,
) -> None:
    height, width = image.shape[:2]
    points = [
        (
            max(0, min(width - 1, int(mark.x * width))),
            max(0, min(height - 1, int(mark.y * height))),
        )
        for mark in reading.landmarks
    ]
    if not points:
        return

    color = CYAN if hand_index == 0 else PURPLE
    if show_landmarks:
        for start, end in HAND_CONNECTIONS:
            cv2.line(image, points[start], points[end], color, 2, cv2.LINE_AA)
        for index, point in enumerate(points):
            radius = 5 if index in (0, 4, 8, 12, 16, 20) else 3
            cv2.circle(image, point, radius + 2, PANEL, -1, cv2.LINE_AA)
            cv2.circle(image, point, radius, color, -1, cv2.LINE_AA)

    padding = 28
    x1 = max(8, min(point[0] for point in points) - padding)
    y1 = max(68, min(point[1] for point in points) - padding)
    x2 = min(width - 8, max(point[0] for point in points) + padding)
    y2 = min(height - 62, max(point[1] for point in points) + padding)
    if x2 > x1 and y2 > y1:
        rounded_rect(image, (x1, y1), (x2, y2), color, 16, 2)

    badge_width = min(240, max(165, x2 - x1))
    badge_y1 = max(68, y1 - 37)
    overlay = image.copy()
    rounded_rect(
        overlay,
        (x1, badge_y1),
        (min(width - 8, x1 + badge_width), badge_y1 + 30),
        PANEL,
        10,
    )
    cv2.addWeighted(overlay, 0.9, image, 0.1, 0, image)
    badge_text = f"{reading.side}  |  {title_case_gesture(reading.gesture)}"
    label(image, badge_text, (x1 + 10, badge_y1 + 20), 0.46, color, 1)


def draw_dashboard(
    image: np.ndarray,
    readings: list[HandReading],
    fps: float,
    paused: bool,
    notice: str,
    notice_until: float,
) -> None:
    height, width = image.shape[:2]

    glass_panel(image, (18, 14), (width - 18, 64), 0.88)
    cv2.circle(image, (42, 39), 8, GREEN if not paused else CYAN, -1, cv2.LINE_AA)
    label(image, "NANON", (62, 45), 0.68, INK, 2)
    label(image, "GESTURE STUDIO", (150, 44), 0.48, MUTED, 1)
    status = "PAUSED" if paused else "LIVE"
    label(image, status, (width - 151, 44), 0.48, CYAN if paused else GREEN, 2)
    label(image, f"{fps:4.0f} FPS", (width - 84, 44), 0.43, MUTED, 1)

    panel_height = 84 + max(1, len(readings)) * 98
    glass_panel(image, (18, 82), (302, min(height - 70, 82 + panel_height)), 0.84)
    label(image, "RECOGNITION", (38, 113), 0.43, MUTED, 1)
    if not readings:
        label(image, "Show your hands", (38, 159), 0.72, INK, 2)
        label(image, "inside the camera frame", (38, 187), 0.43, MUTED, 1)
    else:
        for index, reading in enumerate(readings):
            y = 148 + index * 98
            color = CYAN if index == 0 else PURPLE
            label(image, reading.side.upper(), (38, y), 0.39, color, 1)
            label(image, title_case_gesture(reading.gesture), (38, y + 29), 0.68, INK, 2)
            bar_x1, bar_y, bar_x2 = 38, y + 48, 280
            rounded_rect(image, (bar_x1, bar_y), (bar_x2, bar_y + 9), (52, 57, 72), 4)
            fill = bar_x1 + int((bar_x2 - bar_x1) * max(0.0, min(1.0, reading.confidence)))
            if fill > bar_x1:
                rounded_rect(image, (bar_x1, bar_y), (fill, bar_y + 9), color, 4)
            label(image, f"{reading.confidence * 100:.0f}% confidence", (38, y + 75), 0.4, MUTED, 1)

    footer_y = height - 54
    glass_panel(image, (18, footer_y), (width - 18, height - 14), 0.82)
    shortcuts = "SPACE  pause     S  capture     L  landmarks     H  hide UI     M  mirror     Q  quit"
    label(image, shortcuts, (38, height - 29), 0.43, MUTED, 1)

    if notice and time.monotonic() < notice_until:
        (text_width, _), _ = cv2.getTextSize(
            notice, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
        )
        x1 = max(320, (width - text_width) // 2 - 16)
        x2 = min(width - 22, x1 + text_width + 32)
        glass_panel(image, (x1, 78), (x2, 116), 0.92)
        label(image, notice, (x1 + 16, 103), 0.5, GREEN, 1)


def open_camera(index: int, width: int, height: int) -> cv2.VideoCapture:
    backend = cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY
    camera = cv2.VideoCapture(index, backend)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not camera.isOpened():
        camera.release()
        raise RuntimeError(f"Cannot open camera {index}. Try another device with --camera 1")
    return camera


def create_recognizer(model_path: Path, number_of_hands: int):
    options = mp.tasks.vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=number_of_hands,
        min_hand_detection_confidence=0.55,
        min_hand_presence_confidence=0.55,
        min_tracking_confidence=0.55,
    )
    return mp.tasks.vision.GestureRecognizer.create_from_options(options)


def readings_from(result, smoother: GestureSmoother, threshold: float) -> list[HandReading]:
    readings: list[HandReading] = []
    for index, landmarks in enumerate(result.hand_landmarks):
        side = "Hand"
        if index < len(result.handedness) and result.handedness[index]:
            side = result.handedness[index][0].category_name or side

        gesture_name, score = "None", 0.0
        if index < len(result.gestures) and result.gestures[index]:
            best = result.gestures[index][0]
            gesture_name, score = best.category_name or "None", float(best.score)

        is_confident = gesture_name != "None" and score >= threshold
        display_name = gesture_name if is_confident else "No gesture"
        display_score = score if is_confident else 0.0
        stable_name, stable_score = smoother.update(
            f"{side}-{index}", display_name, display_score
        )
        readings.append(HandReading(side, stable_name, stable_score, landmarks))
    return readings


def run() -> None:
    args = parse_args()
    if not 0.0 <= args.confidence <= 1.0:
        raise ValueError("--confidence must be between 0 and 1")

    model_path = model_path_from(args)
    ensure_model(model_path)
    recognizer = create_recognizer(model_path, args.hands)
    try:
        camera = open_camera(args.camera, args.width, args.height)
    except Exception:
        recognizer.close()
        raise

    smoother = GestureSmoother()
    fps_meter = FpsMeter()
    last_timestamp = 0
    readings: list[HandReading] = []
    paused = False
    mirrored = True
    show_landmarks = True
    show_dashboard = True
    notice = "Camera and model ready"
    notice_until = time.monotonic() + 2.5

    cv2.namedWindow(APP_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(APP_NAME, args.width, args.height)

    try:
        while True:
            success, frame = camera.read()
            if not success:
                raise RuntimeError("The camera stopped returning frames.")
            if mirrored:
                frame = cv2.flip(frame, 1)

            fps = fps_meter.tick()
            if not paused:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                timestamp = max(int(time.perf_counter() * 1000), last_timestamp + 1)
                last_timestamp = timestamp
                result = recognizer.recognize_for_video(mp_image, timestamp)
                readings = readings_from(result, smoother, args.confidence)

            for index, reading in enumerate(readings):
                draw_hand(frame, reading, index, show_landmarks)
            if show_dashboard:
                draw_dashboard(frame, readings, fps, paused, notice, notice_until)

            cv2.imshow(APP_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break
            if key == ord(" "):
                paused = not paused
                notice = "Recognition paused" if paused else "Recognition resumed"
                notice_until = time.monotonic() + 1.5
            elif key == ord("l"):
                show_landmarks = not show_landmarks
                notice = f"Landmarks {'on' if show_landmarks else 'off'}"
                notice_until = time.monotonic() + 1.5
            elif key == ord("h"):
                show_dashboard = not show_dashboard
            elif key == ord("m"):
                mirrored = not mirrored
                smoother.clear()
                notice = f"Mirror {'on' if mirrored else 'off'}"
                notice_until = time.monotonic() + 1.5
            elif key == ord("s"):
                SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
                filename = SCREENSHOT_DIR / time.strftime("gesture_%Y%m%d_%H%M%S.png")
                if cv2.imwrite(str(filename), frame):
                    notice = f"Saved {filename.name}"
                else:
                    notice = "Could not save screenshot"
                notice_until = time.monotonic() + 2.0
    finally:
        camera.release()
        recognizer.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        run()
    except (RuntimeError, ValueError) as error:
        print(f"\n{APP_NAME}: {error}")
        raise SystemExit(1) from error
