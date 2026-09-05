"""Webcam gaze cursor with pinch-to-click hand gestures.

Approximate accessibility / learning prototype, not a medical eye tracker.

Accuracy notes
--------------
The gaze estimate is built from roll- and scale-invariant iris offsets, fitted
to the screen with a regularized quadratic model per eye, then filtered with a
One Euro filter. Head movement after calibration is still the main error
source: press R for a fast 5-point drift fix instead of a full recalibration.

Controls
    C           full recalibration
    R           quick 5-point drift fix (keeps the main fit)
    V           accuracy check on 4 fresh points
    M           enable / disable moving the real mouse cursor
    G           enable / disable hand gestures
    B           show / hide the gaze bubble
    P           show / hide the camera preview
    S           save calibration          L   load saved calibration
    Q / Esc     quit

Gestures (right or left hand, palm toward the camera)
    thumb + index pinch, quick release      left click
    two quick pinches                       double click
    pinch and hold  (> 0.45 s)              press and drag, release to drop
    thumb + middle pinch                    right click

While a pinch is held the cursor is frozen at the point you were looking at
when the pinch started, so the click lands where you aimed.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import math
import os
import tempfile
import time
import tkinter as tk
import urllib.request
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np

APP_NAME = "Eye Tracker"
SCRIPT_DIR = Path(__file__).resolve().parent
CALIBRATION_FILE = Path.home() / ".eye_tracker_calibration.json"

FACE_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
)
HAND_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)

# Face Landmarker indices.
LEFT_IRIS_RING = (468, 469, 470, 471, 472)
RIGHT_IRIS_RING = (473, 474, 475, 476, 477)
LEFT_CORNERS = (33, 133)      # outer, inner
LEFT_LIDS = (159, 145)        # upper, lower
RIGHT_CORNERS = (362, 263)    # inner, outer
RIGHT_LIDS = (386, 374)

# Hand Landmarker indices.
WRIST, THUMB_TIP, INDEX_TIP, MIDDLE_MCP, MIDDLE_TIP = 0, 4, 8, 9, 12

CYAN = "#4de3ff"
GREEN = "#7ceb8a"
AMBER = "#ffd24d"
RED = "#ff7b8b"
WHITE = "#f7f9ff"
DARK = "#111522"
MUTED = (185, 190, 205)


# --------------------------------------------------------------------------
# platform helpers
# --------------------------------------------------------------------------

def enable_dpi_awareness() -> None:
    """Make Tk report physical pixels so overlay and mouse coordinates agree."""
    if os.name != "nt":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # per-monitor aware
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


class Mouse:
    """Absolute cursor moves and button events."""

    MOVE, LEFT_DOWN, LEFT_UP = 0x0001, 0x0002, 0x0004
    RIGHT_DOWN, RIGHT_UP = 0x0008, 0x0010

    def __init__(self) -> None:
        self.backend = "none"
        self._pyautogui = None
        if os.name == "nt":
            self.backend = "windows"
            self._build_structures()
        else:
            try:
                import pyautogui  # noqa: PLC0415

                pyautogui.FAILSAFE = False
                self._pyautogui = pyautogui
                self.backend = "pyautogui"
            except Exception:
                self.backend = "none"

    def _build_structures(self) -> None:
        class MouseInput(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_uint32),
                ("dwFlags", ctypes.c_uint32),
                ("time", ctypes.c_uint32),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
            ]

        class InputUnion(ctypes.Union):
            _fields_ = [("mi", MouseInput)]

        class Input(ctypes.Structure):
            _fields_ = [("type", ctypes.c_uint32), ("union", InputUnion)]

        self._MouseInput = MouseInput
        self._InputUnion = InputUnion
        self._Input = Input

    def _send(self, flags: int) -> None:
        if self.backend != "windows":
            return
        payload = self._Input(
            type=0,
            union=self._InputUnion(
                mi=self._MouseInput(0, 0, 0, flags, 0, ctypes.pointer(ctypes.c_ulong(0)))
            ),
        )
        ctypes.windll.user32.SendInput(1, ctypes.byref(payload), ctypes.sizeof(payload))

    def move(self, x: float, y: float) -> None:
        if self.backend == "windows":
            ctypes.windll.user32.SetCursorPos(int(x), int(y))
        elif self._pyautogui:
            self._pyautogui.moveTo(int(x), int(y), _pause=False)

    def press(self, button: str = "left") -> None:
        if self.backend == "windows":
            self._send(self.LEFT_DOWN if button == "left" else self.RIGHT_DOWN)
        elif self._pyautogui:
            self._pyautogui.mouseDown(button=button, _pause=False)

    def release(self, button: str = "left") -> None:
        if self.backend == "windows":
            self._send(self.LEFT_UP if button == "left" else self.RIGHT_UP)
        elif self._pyautogui:
            self._pyautogui.mouseUp(button=button, _pause=False)

    def click(self, button: str = "left") -> None:
        self.press(button)
        time.sleep(0.012)
        self.release(button)


# --------------------------------------------------------------------------
# setup
# --------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--camera", type=int, default=0, help="camera device index")
    parser.add_argument("--model", type=Path, help="path to face_landmarker.task")
    parser.add_argument("--hand-model", type=Path, help="path to hand_landmarker.task")
    parser.add_argument("--width", type=int, default=1280, help="capture width")
    parser.add_argument("--height", type=int, default=720, help="capture height")
    parser.add_argument("--points", type=int, default=13, choices=(9, 13, 16),
                        help="number of calibration targets")
    parser.add_argument("--smooth", type=float, default=0.25,
                        help="0.05 steady and laggy, 1.0 twitchy and fast")
    parser.add_argument("--ridge", type=float, default=0.06,
                        help="calibration regularization, raise it if the bubble overshoots")
    parser.add_argument("--pinch-close", type=float, default=0.36, help="pinch closes below this")
    parser.add_argument("--pinch-open", type=float, default=0.55, help="pinch opens above this")
    parser.add_argument("--hand-every", type=int, default=2,
                        help="run hand tracking every Nth frame")
    parser.add_argument("--no-hands", action="store_true", help="disable gestures")
    parser.add_argument("--no-mouse", action="store_true", help="do not move the real cursor")
    parser.add_argument("--no-preview", action="store_true", help="start with preview hidden")
    parser.add_argument("--no-load", action="store_true", help="ignore any saved calibration")
    return parser.parse_args()


def find_model(custom: Path | None, filename: str) -> Path:
    if custom:
        return custom.expanduser().resolve()
    candidates = (SCRIPT_DIR / filename, SCRIPT_DIR.parent / filename)
    return next((path for path in candidates if path.exists()), candidates[0])


def ensure_model(path: Path, url: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {path.name} ...")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=path.parent, suffix=".download") as file:
            temporary = Path(file.name)
        urllib.request.urlretrieve(url, temporary)
        temporary.replace(path)
        print("Model ready.")
    except Exception as error:
        if temporary and temporary.exists():
            temporary.unlink()
        raise RuntimeError(
            f"Model download failed. Download it from\n{url}\nand save it as {path}"
        ) from error


def open_camera(index: int, width: int, height: int) -> cv2.VideoCapture:
    backends = (
        (cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY) if os.name == "nt" else (cv2.CAP_ANY,)
    )
    for backend in backends:
        camera = cv2.VideoCapture(index, backend)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        camera.set(cv2.CAP_PROP_FPS, 30)
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # A hunting autofocus blurs the iris and adds several pixels of noise.
        camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        if camera.isOpened():
            for _ in range(8):
                success, frame = camera.read()
                if success and frame is not None and frame.size and float(np.mean(frame)) > 2.0:
                    return camera
        camera.release()
    raise RuntimeError(f"Could not read camera {index}. Try --camera 1")


def create_face_landmarker(model_path: Path):
    options = mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_faces=1,
        output_facial_transformation_matrixes=True,
        min_face_detection_confidence=0.6,
        min_face_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    return mp.tasks.vision.FaceLandmarker.create_from_options(options)


def create_hand_landmarker(model_path: Path):
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.6,
    )
    return mp.tasks.vision.HandLandmarker.create_from_options(options)


# --------------------------------------------------------------------------
# gaze features
# --------------------------------------------------------------------------

@dataclass
class EyeReading:
    """One frame of eye measurements, in head-relative units."""

    left: tuple[float, float]
    right: tuple[float, float]
    openness: float
    yaw: float
    pitch: float
    roll: float
    scale: float
    left_iris: tuple[int, int]
    right_iris: tuple[int, int]

    def vector(self) -> np.ndarray:
        return np.array(
            [self.left[0], self.left[1], self.right[0], self.right[1],
             self.yaw, self.pitch], dtype=float
        )


def landmark_array(landmarks, width: int, height: int) -> np.ndarray:
    """Pixel-space landmarks so that x and y share one isotropic scale."""
    return np.array([[point.x * width, point.y * height] for point in landmarks], dtype=float)


def single_eye(points: np.ndarray, ring, corners, lids) -> tuple[float, float, float, np.ndarray]:
    """Iris offset expressed in the eye's own frame.

    The eye-corner line defines the local x-axis, so head roll cancels out, and
    both offsets are divided by the eye width, so camera distance cancels out.
    Dividing the vertical offset by the eye *width* rather than the eyelid gap
    is the important part: the eyelid gap is only a few pixels tall and moves
    with every blink, which is what makes naive vertical gaze so noisy.
    """
    iris = points[list(ring)].mean(axis=0)
    first, second = points[corners[0]], points[corners[1]]
    center = (first + second) / 2.0
    axis = second - first
    if axis[0] < 0:
        axis = -axis
    width = float(np.linalg.norm(axis))
    if width < 1e-6:
        raise ValueError("degenerate eye")
    unit_x = axis / width
    unit_y = np.array([-unit_x[1], unit_x[0]])
    delta = iris - center
    dx = float(delta @ unit_x) / width
    dy = float(delta @ unit_y) / width
    openness = float(np.linalg.norm(points[lids[0]] - points[lids[1]])) / width
    return dx, dy, openness, iris


def head_pose(matrix: np.ndarray | None) -> tuple[float, float, float]:
    """Yaw, pitch and roll in radians from the facial transformation matrix."""
    if matrix is None:
        return 0.0, 0.0, 0.0
    rotation = np.asarray(matrix, dtype=float)[:3, :3]
    norms = np.linalg.norm(rotation, axis=0)
    norms[norms < 1e-9] = 1.0
    rotation = rotation / norms
    pitch = math.atan2(rotation[2, 1], rotation[2, 2])
    yaw = math.atan2(-rotation[2, 0], math.hypot(rotation[2, 1], rotation[2, 2]))
    roll = math.atan2(rotation[1, 0], rotation[0, 0])
    return yaw, pitch, roll


def read_eyes(landmarks, matrix, width: int, height: int) -> EyeReading | None:
    if len(landmarks) <= RIGHT_IRIS_RING[-1]:
        return None
    points = landmark_array(landmarks, width, height)
    try:
        left_dx, left_dy, left_open, left_iris = single_eye(
            points, LEFT_IRIS_RING, LEFT_CORNERS, LEFT_LIDS
        )
        right_dx, right_dy, right_open, right_iris = single_eye(
            points, RIGHT_IRIS_RING, RIGHT_CORNERS, RIGHT_LIDS
        )
    except ValueError:
        return None
    yaw, pitch, roll = head_pose(matrix)
    eye_span = float(np.linalg.norm(points[LEFT_CORNERS[0]] - points[RIGHT_CORNERS[1]]))
    return EyeReading(
        left=(left_dx, left_dy),
        right=(right_dx, right_dy),
        openness=(left_open + right_open) / 2.0,
        yaw=yaw,
        pitch=pitch,
        roll=roll,
        scale=eye_span,
        left_iris=(int(left_iris[0]), int(left_iris[1])),
        right_iris=(int(right_iris[0]), int(right_iris[1])),
    )


class OpennessGate:
    """Reject blinks and half-lidded frames relative to this user's own eyes."""

    def __init__(self) -> None:
        self.history: deque[float] = deque(maxlen=180)

    def accept(self, openness: float) -> bool:
        self.history.append(openness)
        if len(self.history) < 12:
            return openness > 0.16
        baseline = float(np.percentile(np.asarray(self.history), 85))
        return openness > max(0.14, 0.62 * baseline)


# --------------------------------------------------------------------------
# mapping
# --------------------------------------------------------------------------

class GazeMapper:
    """Ridge-regularized quadratic mapping, fitted separately for each eye."""

    # bias is handled outside the design matrix
    PENALTY = np.array([0.3, 0.3, 1.0, 2.0, 2.0, 4.0, 4.0])

    def __init__(self, ridge: float = 0.06) -> None:
        self.ridge = ridge
        self.models: list[dict] = []
        self.reference = (0.0, 0.0)
        self.affine: np.ndarray | None = None
        self.residual = float("nan")

    @staticmethod
    def features(dx: float, dy: float, dyaw: float, dpitch: float) -> list[float]:
        return [dx, dy, dx * dy, dx * dx, dy * dy, dyaw, dpitch]

    @property
    def ready(self) -> bool:
        return bool(self.models)

    def fit(self, samples: list[np.ndarray], targets: list[tuple[int, int]]) -> float:
        """samples rows are [ldx, ldy, rdx, rdy, yaw, pitch]."""
        data = np.asarray(samples, dtype=float)
        screen = np.asarray(targets, dtype=float)
        self.reference = (float(np.median(data[:, 4])), float(np.median(data[:, 5])))
        self.models = []
        for offset in (0, 2):
            design = np.asarray([
                self.features(
                    row[offset], row[offset + 1],
                    row[4] - self.reference[0], row[5] - self.reference[1],
                )
                for row in data
            ])
            self.models.append(self._solve(design, screen))
        self.affine = None
        predicted = np.asarray([
            self._predict_raw(row[0], row[1], row[2], row[3], row[4], row[5])
            for row in data
        ])
        self.residual = float(np.sqrt(np.mean(np.sum((predicted - screen) ** 2, axis=1))))
        return self.residual

    def _solve(self, design: np.ndarray, screen: np.ndarray) -> dict:
        mean = design.mean(axis=0)
        deviation = design.std(axis=0)
        deviation[deviation < 1e-9] = 1.0
        centered = (design - mean) / deviation
        gram = centered.T @ centered + self.ridge * len(design) * np.diag(self.PENALTY)
        weights = np.linalg.solve(gram, centered.T @ (screen - screen.mean(axis=0)))
        return {
            "mean": mean,
            "deviation": deviation,
            "weights": weights,
            "intercept": screen.mean(axis=0),
        }

    def _apply(self, model: dict, feature: list[float]) -> np.ndarray:
        vector = (np.asarray(feature) - model["mean"]) / model["deviation"]
        return model["intercept"] + vector @ model["weights"]

    def _predict_raw(self, ldx, ldy, rdx, rdy, yaw, pitch) -> np.ndarray:
        dyaw = yaw - self.reference[0]
        dpitch = pitch - self.reference[1]
        left = self._apply(self.models[0], self.features(ldx, ldy, dyaw, dpitch))
        right = self._apply(self.models[1], self.features(rdx, rdy, dyaw, dpitch))
        return (left + right) / 2.0

    def predict(self, reading: EyeReading, width: int, height: int) -> tuple[float, float]:
        if not self.models:
            return width / 2.0, height / 2.0
        point = self._predict_raw(
            reading.left[0], reading.left[1], reading.right[0], reading.right[1],
            reading.yaw, reading.pitch,
        )
        if self.affine is not None:
            point = np.array([point[0], point[1], 1.0]) @ self.affine
        margin = 6
        return (
            float(np.clip(point[0], margin, width - margin)),
            float(np.clip(point[1], margin, height - margin)),
        )

    def fit_drift(self, predicted: list[tuple[float, float]],
                  targets: list[tuple[int, int]]) -> float:
        """Correct slow drift with an affine nudge, keeping the main fit."""
        source = np.asarray([[x, y, 1.0] for x, y in predicted], dtype=float)
        screen = np.asarray(targets, dtype=float)
        affine, _, _, _ = np.linalg.lstsq(source, screen, rcond=None)
        self.affine = affine
        corrected = source @ affine
        return float(np.sqrt(np.mean(np.sum((corrected - screen) ** 2, axis=1))))

    def to_dict(self, width: int, height: int) -> dict:
        return {
            "screen": [width, height],
            "reference": list(self.reference),
            "residual": self.residual,
            "affine": None if self.affine is None else self.affine.tolist(),
            "models": [
                {
                    "mean": model["mean"].tolist(),
                    "deviation": model["deviation"].tolist(),
                    "weights": model["weights"].tolist(),
                    "intercept": model["intercept"].tolist(),
                }
                for model in self.models
            ],
        }

    def load_dict(self, payload: dict, width: int, height: int) -> bool:
        if payload.get("screen") != [width, height] or not payload.get("models"):
            return False
        self.reference = tuple(payload["reference"])
        self.residual = float(payload.get("residual", float("nan")))
        affine = payload.get("affine")
        self.affine = None if affine is None else np.asarray(affine, dtype=float)
        self.models = [
            {
                "mean": np.asarray(model["mean"], dtype=float),
                "deviation": np.asarray(model["deviation"], dtype=float),
                "weights": np.asarray(model["weights"], dtype=float),
                "intercept": np.asarray(model["intercept"], dtype=float),
            }
            for model in payload["models"]
        ]
        return True


class OneEuroFilter:
    """Low lag when the eye jumps, low jitter when it rests."""

    def __init__(self, min_cutoff: float, beta: float, derivative_cutoff: float = 1.0) -> None:
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.derivative_cutoff = derivative_cutoff
        self.previous: np.ndarray | None = None
        self.speed = np.zeros(2)
        self.timestamp = 0.0

    @staticmethod
    def _alpha(cutoff: float, dt: float) -> float:
        tau = 1.0 / (2.0 * math.pi * cutoff)
        return 1.0 / (1.0 + tau / dt)

    def reset(self, value: np.ndarray | None = None) -> None:
        self.previous = None if value is None else np.asarray(value, dtype=float)
        self.speed = np.zeros(2)
        self.timestamp = time.monotonic()

    def __call__(self, value: tuple[float, float]) -> np.ndarray:
        now = time.monotonic()
        current = np.asarray(value, dtype=float)
        if self.previous is None:
            self.previous, self.timestamp = current, now
            return current
        dt = max(now - self.timestamp, 1e-3)
        self.timestamp = now
        raw_speed = (current - self.previous) / dt
        speed_alpha = self._alpha(self.derivative_cutoff, dt)
        self.speed += speed_alpha * (raw_speed - self.speed)
        cutoff = self.min_cutoff + self.beta * float(np.linalg.norm(self.speed))
        alpha = self._alpha(cutoff, dt)
        self.previous += alpha * (current - self.previous)
        return self.previous.copy()


# --------------------------------------------------------------------------
# calibration
# --------------------------------------------------------------------------

def make_targets(width: int, height: int, count: int) -> list[tuple[int, int]]:
    mx, my = int(width * 0.06), int(height * 0.08)
    columns = [mx, width // 2, width - mx]
    rows = [my, height // 2, height - my]
    grid = [(x, y) for y in rows for x in columns]
    if count >= 13:
        grid += [
            (int(width * 0.28), int(height * 0.30)),
            (int(width * 0.72), int(height * 0.30)),
            (int(width * 0.28), int(height * 0.70)),
            (int(width * 0.72), int(height * 0.70)),
        ]
    if count >= 16:
        grid += [
            (int(width * 0.50), int(height * 0.28)),
            (int(width * 0.28), int(height * 0.50)),
            (int(width * 0.72), int(height * 0.50)),
        ]
    center = grid.pop(4)
    return [center, *grid]


def robust_median(samples: list[np.ndarray]) -> np.ndarray:
    """Median after dropping samples more than 2.5 MAD from it."""
    values = np.asarray(samples, dtype=float)
    median = np.median(values, axis=0)
    spread = np.median(np.abs(values - median), axis=0)
    spread[spread < 1e-9] = 1e-9
    keep = np.all(np.abs(values - median) <= 2.5 * spread * 1.4826 + 1e-6, axis=1)
    if keep.sum() >= max(5, len(values) // 3):
        median = np.median(values[keep], axis=0)
    return median


@dataclass
class Calibration:
    targets: list[tuple[int, int]]
    mode: str = "full"           # full | drift | validate
    settle: float = 0.55
    sample: float = 0.80
    active: bool = False
    index: int = 0
    started: float = 0.0
    samples: list[np.ndarray] = field(default_factory=list)
    collected: list[np.ndarray] = field(default_factory=list)
    errors: list[float] = field(default_factory=list)

    def start(self) -> None:
        self.active = True
        self.index = 0
        self.samples.clear()
        self.collected.clear()
        self.errors.clear()
        self.started = time.monotonic()

    @property
    def target(self) -> tuple[int, int]:
        return self.targets[self.index]

    @property
    def progress(self) -> float:
        elapsed = time.monotonic() - self.started
        return float(np.clip((elapsed - self.settle) / self.sample, 0.0, 1.0))

    def update(self, sample: np.ndarray | None) -> bool:
        """Return True on the frame where the last target completes."""
        if not self.active:
            return False
        elapsed = time.monotonic() - self.started
        if sample is not None and elapsed >= self.settle:
            self.samples.append(sample)
        if elapsed < self.settle + self.sample:
            return False
        if len(self.samples) < 8:
            # The face was lost, so retry this target instead of skipping it.
            self.samples.clear()
            self.started = time.monotonic()
            return False

        value = robust_median(self.samples)
        self.collected.append(value)
        if self.mode == "validate":
            target = np.asarray(self.target, dtype=float)
            self.errors.append(float(np.linalg.norm(value - target)))
        self.samples.clear()
        self.index += 1
        self.started = time.monotonic()
        if self.index >= len(self.targets):
            self.active = False
            return True
        return False


# --------------------------------------------------------------------------
# hand gestures
# --------------------------------------------------------------------------

@dataclass
class GestureEvent:
    kind: str               # click | double | right | drag_start | drag_end
    at: tuple[float, float]


class PinchDetector:
    """Hysteresis on a size-normalized pinch distance."""

    def __init__(self, close: float, open_: float, tip: int) -> None:
        self.close = close
        self.open = open_
        self.tip = tip
        self.pinched = False
        self.ratio = 1.0

    def update(self, points: np.ndarray | None) -> bool:
        if points is None:
            self.pinched = False
            self.ratio = 1.0
            return False
        scale = float(np.linalg.norm(points[WRIST] - points[MIDDLE_MCP]))
        if scale < 1e-6:
            return self.pinched
        self.ratio = float(np.linalg.norm(points[THUMB_TIP] - points[self.tip])) / scale
        if self.pinched and self.ratio > self.open:
            self.pinched = False
        elif not self.pinched and self.ratio < self.close:
            self.pinched = True
        return self.pinched


class GestureController:
    HOLD_SECONDS = 0.45
    DOUBLE_SECONDS = 0.45
    COOLDOWN = 0.18

    def __init__(self, close: float, open_: float) -> None:
        self.left = PinchDetector(close, open_, INDEX_TIP)
        self.right = PinchDetector(close, open_, MIDDLE_TIP)
        self.anchor: tuple[float, float] | None = None
        self.down_at = 0.0
        self.dragging = False
        self.last_click = 0.0
        self.last_anchor: tuple[float, float] | None = None
        self.last_event = ""
        self.event_time = 0.0
        self.right_active = False

    @property
    def holding(self) -> bool:
        return self.anchor is not None

    def update(self, points: np.ndarray | None,
               gaze: tuple[float, float]) -> list[GestureEvent]:
        now = time.monotonic()
        events: list[GestureEvent] = []
        index_pinched = self.left.update(points)
        middle_pinched = self.right.update(points) and not index_pinched

        # right click: thumb and middle finger
        if middle_pinched and not self.right_active and not self.holding:
            if now - self.last_click > self.COOLDOWN:
                events.append(GestureEvent("right", gaze))
                self.last_click = now
            self.right_active = True
        elif not middle_pinched:
            self.right_active = False

        if index_pinched and self.anchor is None:
            # Reuse the previous anchor so a fast second pinch registers as a
            # real double click instead of two clicks a few pixels apart.
            reuse = (
                self.last_anchor is not None
                and now - self.last_click < self.DOUBLE_SECONDS
            )
            self.anchor = self.last_anchor if reuse else gaze
            self.down_at = now
        elif index_pinched and self.anchor is not None:
            if not self.dragging and now - self.down_at > self.HOLD_SECONDS:
                self.dragging = True
                events.append(GestureEvent("drag_start", self.anchor))
        elif not index_pinched and self.anchor is not None:
            if self.dragging:
                events.append(GestureEvent("drag_end", gaze))
                self.dragging = False
            elif now - self.last_click < self.DOUBLE_SECONDS:
                events.append(GestureEvent("double", self.anchor))
            else:
                events.append(GestureEvent("click", self.anchor))
            self.last_anchor = self.anchor
            self.last_click = now
            self.anchor = None

        if events:
            self.last_event = events[-1].kind
            self.event_time = now
        return events

    def recent_event(self) -> str:
        if self.last_event and time.monotonic() - self.event_time < 0.8:
            return self.last_event
        return ""


def hand_points(landmarks, width: int, height: int) -> np.ndarray:
    return np.array([[point.x * width, point.y * height] for point in landmarks], dtype=float)


# --------------------------------------------------------------------------
# overlay
# --------------------------------------------------------------------------

class GazeOverlay:
    """Transparent, always-on-top overlay that does not consume mouse clicks."""

    TRANSPARENT = "#010203"

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.attributes("-topmost", True)
        self.root.configure(bg=self.TRANSPARENT)
        if os.name == "nt":
            self.root.attributes("-transparentcolor", self.TRANSPARENT)
        else:
            self.root.attributes("-alpha", 0.82)
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height,
            bg=self.TRANSPARENT, highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)
        # The native top-level window does not exist until Tk processes one
        # complete update; applying transparency earlier can leave a nearly
        # black fullscreen window on some Windows/Tk versions.
        self.root.update_idletasks()
        self.root.update()
        if os.name == "nt":
            self.root.attributes("-transparentcolor", self.TRANSPARENT)
        self._make_click_through()

    def _make_click_through(self) -> None:
        if os.name != "nt":
            return
        try:
            user32 = ctypes.windll.user32
            client_hwnd = self.root.winfo_id()
            get_parent = user32.GetParent
            get_parent.argtypes = (ctypes.c_void_p,)
            get_parent.restype = ctypes.c_void_p
            hwnd = get_parent(client_hwnd) or client_hwnd
            get_style, set_style = user32.GetWindowLongW, user32.SetWindowLongW
            get_style.argtypes = (ctypes.c_void_p, ctypes.c_int)
            get_style.restype = ctypes.c_long
            set_style.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_long)
            set_style.restype = ctypes.c_long
            extended = get_style(hwnd, -20)
            # WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_NOACTIVATE
            set_style(hwnd, -20, extended | 0x80000 | 0x20 | 0x08000000)
            set_layered = user32.SetLayeredWindowAttributes
            set_layered.argtypes = (
                ctypes.c_void_p, ctypes.c_uint, ctypes.c_ubyte, ctypes.c_uint
            )
            set_layered.restype = ctypes.c_int
            if not set_layered(hwnd, 0x030201, 255, 0x00000001):  # LWA_COLORKEY
                raise OSError("Windows could not enable overlay transparency")
        except (AttributeError, OSError):
            self.root.withdraw()
            raise RuntimeError(
                "The transparent desktop overlay is unavailable on this Windows setup"
            )

    def clear(self) -> None:
        self.canvas.delete("all")

    def _banner(self, title: str, subtitle: str, color: str) -> None:
        self.canvas.create_rectangle(
            self.width // 2 - 230, 24, self.width // 2 + 230, 104, fill=DARK, outline=""
        )
        self.canvas.create_text(
            self.width // 2, 49, text=title, fill=WHITE, font=("Segoe UI Semibold", 16)
        )
        self.canvas.create_text(
            self.width // 2, 79, text=subtitle, fill=color, font=("Segoe UI", 11)
        )

    def show_calibration(self, calibration: Calibration, face_visible: bool) -> None:
        self.clear()
        x, y = calibration.target
        radius = 20
        self.canvas.create_oval(
            x - radius - 8, y - radius - 8, x + radius + 8, y + radius + 8,
            outline=DARK, width=7,
        )
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=CYAN, outline=WHITE, width=4,
        )
        # A small centre dot gives the eye something precise to land on.
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=DARK, outline="")
        sweep = max(1, int(359 * calibration.progress))
        self.canvas.create_arc(
            x - 40, y - 40, x + 40, y + 40,
            start=90, extent=-sweep, style="arc", outline=WHITE, width=6,
        )
        titles = {
            "full": "LOOK AT THE DOT",
            "drift": "DRIFT FIX - LOOK AT THE DOT",
            "validate": "ACCURACY CHECK - LOOK AT THE DOT",
        }
        subtitle = (
            f"{calibration.index + 1} of {len(calibration.targets)}  -  keep your head still"
            if face_visible else "Move into the camera view"
        )
        self._banner(titles[calibration.mode], subtitle, CYAN if face_visible else RED)

    def show_bubble(self, x: float, y: float, visible: bool, status: str = "",
                    color: str = CYAN, frozen: bool = False, flash: str = "") -> None:
        self.clear()
        if visible:
            outer = 32 if frozen else 28
            self.canvas.create_oval(
                x - outer, y - outer, x + outer, y + outer, outline="#132331", width=7
            )
            radius = 15
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=color, outline=WHITE, width=3,
            )
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=WHITE, outline="")
            if frozen:
                self.canvas.create_oval(
                    x - outer - 7, y - outer - 7, x + outer + 7, y + outer + 7,
                    outline=AMBER, width=3,
                )
            if flash:
                self.canvas.create_text(
                    x, y - outer - 22, text=flash.upper(), fill=AMBER,
                    font=("Segoe UI Semibold", 11),
                )
        if status:
            width = 22 + 8 * len(status)
            self.canvas.create_rectangle(22, 20, 22 + width, 62, fill=DARK, outline="")
            self.canvas.create_text(
                38, 41, anchor="w", text=status, fill=WHITE, font=("Segoe UI", 11)
            )

    def update(self) -> None:
        self.root.update_idletasks()
        self.root.update()

    def close(self) -> None:
        try:
            self.root.destroy()
        except tk.TclError:
            pass


class KeyMonitor:
    """Edge-triggered global shortcuts on Windows, where the overlay has no focus."""

    WINDOWS_KEYS = {
        0x1B: "quit", 0x51: "quit", 0x43: "calibrate", 0x52: "drift",
        0x56: "validate", 0x42: "bubble", 0x50: "preview", 0x4D: "mouse",
        0x47: "gestures", 0x53: "save", 0x4C: "load",
    }
    LOCAL_KEYS = {
        27: "quit", ord("q"): "quit", ord("c"): "calibrate", ord("r"): "drift",
        ord("v"): "validate", ord("b"): "bubble", ord("p"): "preview",
        ord("m"): "mouse", ord("g"): "gestures", ord("s"): "save", ord("l"): "load",
    }

    def __init__(self) -> None:
        self.was_down = {key: False for key in self.WINDOWS_KEYS}

    def poll(self, opencv_key: int) -> set[str]:
        actions: set[str] = set()
        if opencv_key in self.LOCAL_KEYS:
            actions.add(self.LOCAL_KEYS[opencv_key])
        if os.name == "nt":
            for virtual_key, name in self.WINDOWS_KEYS.items():
                is_down = bool(ctypes.windll.user32.GetAsyncKeyState(virtual_key) & 0x8000)
                if is_down and not self.was_down[virtual_key]:
                    actions.add(name)
                self.was_down[virtual_key] = is_down
        return actions


def draw_preview(frame: np.ndarray, reading: EyeReading | None, hand: np.ndarray | None,
                 gestures: GestureController | None, calibrated: bool, calibrating: bool,
                 mouse_on: bool, fps: float, accuracy: str, drift_warning: bool) -> np.ndarray:
    output = frame.copy()
    height, width = output.shape[:2]
    panel = output.copy()
    cv2.rectangle(panel, (0, 0), (width, 96), (17, 21, 34), -1)
    cv2.addWeighted(panel, 0.88, output, 0.12, 0, output)

    if reading:
        for point in (reading.left_iris, reading.right_iris):
            cv2.circle(output, point, 11, (30, 35, 45), -1, cv2.LINE_AA)
            cv2.circle(output, point, 5, (255, 227, 77), -1, cv2.LINE_AA)
        status, color = (
            ("CALIBRATING", (255, 227, 77)) if calibrating
            else ("GAZE ACTIVE", (112, 235, 125)) if calibrated
            else ("NOT CALIBRATED", (90, 170, 255))
        )
    else:
        status, color = "FACE NOT FOUND", (95, 95, 245)

    if hand is not None:
        for index in (WRIST, THUMB_TIP, INDEX_TIP, MIDDLE_MCP, MIDDLE_TIP):
            cv2.circle(output, tuple(hand[index].astype(int)), 6, (255, 190, 90), -1, cv2.LINE_AA)
        cv2.line(output, tuple(hand[THUMB_TIP].astype(int)),
                 tuple(hand[INDEX_TIP].astype(int)), (255, 190, 90), 2, cv2.LINE_AA)

    cv2.putText(output, "EYE TRACKER", (24, 32), cv2.FONT_HERSHEY_SIMPLEX,
                0.67, (245, 247, 255), 2, cv2.LINE_AA)
    cv2.putText(output, f"{status}   {fps:4.1f} fps", (24, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 1, cv2.LINE_AA)

    detail = f"mouse {'ON' if mouse_on else 'off'}"
    if gestures:
        detail += f"   pinch {gestures.left.ratio:0.2f}"
        event = gestures.recent_event()
        if event:
            detail += f"   {event.upper()}"
    if accuracy:
        detail += f"   {accuracy}"
    cv2.putText(output, detail, (24, 84), cv2.FONT_HERSHEY_SIMPLEX,
                0.44, MUTED, 1, cv2.LINE_AA)

    if drift_warning:
        cv2.putText(output, "HEAD MOVED - press R", (24, height - 44),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (90, 190, 255), 2, cv2.LINE_AA)

    help_text = "C recal  R drift  V check  M mouse  G gestures  B bubble  P preview  Q quit"
    cv2.putText(output, help_text, (18, height - 16),
                cv2.FONT_HERSHEY_SIMPLEX, 0.40, MUTED, 1, cv2.LINE_AA)
    return output


# --------------------------------------------------------------------------
# main loop
# --------------------------------------------------------------------------

def run() -> None:
    args = parse_args()
    if not 0.05 <= args.smooth <= 1.0:
        raise ValueError("--smooth must be between 0.05 and 1")

    enable_dpi_awareness()

    face_path = find_model(args.model, "face_landmarker.task")
    ensure_model(face_path, FACE_MODEL_URL)
    landmarker = create_face_landmarker(face_path)

    hands = None
    if not args.no_hands:
        hand_path = find_model(args.hand_model, "hand_landmarker.task")
        ensure_model(hand_path, HAND_MODEL_URL)
        hands = create_hand_landmarker(hand_path)

    try:
        camera = open_camera(args.camera, args.width, args.height)
    except Exception:
        landmarker.close()
        if hands:
            hands.close()
        raise

    overlay = GazeOverlay()
    mouse = Mouse()
    mapper = GazeMapper(ridge=args.ridge)
    gate = OpennessGate()
    gestures = GestureController(args.pinch_close, args.pinch_open) if hands else None
    smoother = OneEuroFilter(
        min_cutoff=0.4 + 3.0 * args.smooth,
        beta=0.006 + 0.02 * args.smooth,
    )

    full_targets = make_targets(overlay.width, overlay.height, args.points)
    drift_targets = [
        (int(overlay.width * 0.07), int(overlay.height * 0.10)),
        (int(overlay.width * 0.93), int(overlay.height * 0.10)),
        (overlay.width // 2, overlay.height // 2),
        (int(overlay.width * 0.07), int(overlay.height * 0.90)),
        (int(overlay.width * 0.93), int(overlay.height * 0.90)),
    ]
    check_targets = [
        (int(overlay.width * 0.20), int(overlay.height * 0.22)),
        (int(overlay.width * 0.80), int(overlay.height * 0.38)),
        (int(overlay.width * 0.35), int(overlay.height * 0.78)),
        (int(overlay.width * 0.65), int(overlay.height * 0.62)),
    ]

    calibration = Calibration(full_targets, mode="full")
    loaded = False
    if not args.no_load and CALIBRATION_FILE.exists():
        try:
            payload = json.loads(CALIBRATION_FILE.read_text())
            loaded = mapper.load_dict(payload, overlay.width, overlay.height)
        except (OSError, ValueError, KeyError):
            loaded = False
    if loaded:
        print(f"Loaded calibration from {CALIBRATION_FILE}. Press C to redo it, R to fix drift.")
    else:
        calibration.start()

    feature_history: deque[np.ndarray] = deque(maxlen=3)
    bubble = np.array([overlay.width / 2.0, overlay.height / 2.0])
    bubble_enabled = True
    mouse_enabled = not args.no_mouse and mouse.backend != "none"
    gestures_enabled = gestures is not None
    preview_visible = not args.no_preview
    keys = KeyMonitor()
    last_timestamp = 0
    frame_index = 0
    window_created = False
    fps = 0.0
    last_frame_time = time.monotonic()
    accuracy_text = (
        f"fit {mapper.residual:.0f}px"
        if mapper.ready and not math.isnan(mapper.residual) else ""
    )
    hand_landmarks: np.ndarray | None = None

    if mouse.backend == "none":
        print("No mouse backend available. Install pyautogui for cursor control on this OS.")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                raise RuntimeError("The camera stopped returning frames")
            frame = cv2.flip(frame, 1)
            height, width = frame.shape[:2]
            frame_index += 1

            now = time.monotonic()
            fps = 0.9 * fps + 0.1 / max(now - last_frame_time, 1e-3)
            last_frame_time = now

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp = max(int(time.perf_counter() * 1000), last_timestamp + 1)
            last_timestamp = timestamp
            face_result = landmarker.detect_for_video(mp_image, timestamp)

            reading = None
            if face_result.face_landmarks:
                matrix = None
                matrices = getattr(face_result, "facial_transformation_matrixes", None)
                if matrices:
                    matrix = np.asarray(matrices[0])
                reading = read_eyes(face_result.face_landmarks[0], matrix, width, height)

            usable = None
            if reading is not None and gate.accept(reading.openness):
                feature_history.append(reading.vector())
                # A short median kills single-frame iris spikes without adding lag.
                smoothed = np.median(np.asarray(feature_history), axis=0)
                usable = EyeReading(
                    left=(smoothed[0], smoothed[1]),
                    right=(smoothed[2], smoothed[3]),
                    openness=reading.openness,
                    yaw=smoothed[4], pitch=smoothed[5], roll=reading.roll,
                    scale=reading.scale,
                    left_iris=reading.left_iris, right_iris=reading.right_iris,
                )

            if hands and gestures_enabled and frame_index % max(1, args.hand_every) == 0:
                hand_result = hands.detect_for_video(mp_image, timestamp)
                hand_landmarks = (
                    hand_points(hand_result.hand_landmarks[0], width, height)
                    if hand_result.hand_landmarks else None
                )
            elif not gestures_enabled:
                hand_landmarks = None

            drift_warning = False
            if mapper.ready and usable is not None:
                drift_warning = (
                    abs(usable.yaw - mapper.reference[0]) > math.radians(11)
                    or abs(usable.pitch - mapper.reference[1]) > math.radians(9)
                )

            # ---------------- calibration phases ----------------
            if calibration.active:
                if calibration.mode == "full":
                    sample = usable.vector() if usable is not None else None
                else:
                    sample = (
                        np.asarray(mapper.predict(usable, overlay.width, overlay.height))
                        if usable is not None and mapper.ready else None
                    )
                if calibration.update(sample):
                    if calibration.mode == "full":
                        residual = mapper.fit(calibration.collected, calibration.targets)
                        accuracy_text = f"fit {residual:.0f}px"
                        print(f"Calibration fit residual: {residual:.1f} px")
                    elif calibration.mode == "drift":
                        residual = mapper.fit_drift(
                            [tuple(point) for point in calibration.collected],
                            calibration.targets,
                        )
                        accuracy_text = f"drift {residual:.0f}px"
                        print(f"Drift fix residual: {residual:.1f} px")
                    else:
                        mean_error = float(np.mean(calibration.errors))
                        percent = 100.0 * mean_error / overlay.width
                        accuracy_text = f"check {mean_error:.0f}px"
                        print(
                            f"Accuracy check: {mean_error:.1f} px average "
                            f"({percent:.1f}% of screen width)"
                        )
                    feature_history.clear()
                    smoother.reset()
                else:
                    overlay.show_calibration(calibration, usable is not None)
                    overlay.update()
                    window_created = _pump_preview(
                        preview_visible, frame, usable, hand_landmarks, gestures,
                        mapper.ready, True, mouse_enabled, fps, accuracy_text,
                        drift_warning, window_created,
                    )
                    actions = keys.poll(cv2.waitKey(1) & 0xFF)
                    if "quit" in actions:
                        break
                    continue

            # ---------------- live gaze ----------------
            gaze_point = None
            if usable is not None and mapper.ready:
                predicted = mapper.predict(usable, overlay.width, overlay.height)
                bubble = smoother(predicted)
                gaze_point = (float(bubble[0]), float(bubble[1]))

            # ---------------- gestures ----------------
            frozen = False
            flash = ""
            if gestures and gestures_enabled:
                reference_point = gaze_point or (float(bubble[0]), float(bubble[1]))
                for event in gestures.update(hand_landmarks, reference_point):
                    if mouse_enabled:
                        mouse.move(*event.at)
                        if event.kind == "click":
                            mouse.click("left")
                        elif event.kind == "double":
                            mouse.click("left")
                            time.sleep(0.04)
                            mouse.click("left")
                        elif event.kind == "right":
                            mouse.click("right")
                        elif event.kind == "drag_start":
                            mouse.press("left")
                        elif event.kind == "drag_end":
                            mouse.release("left")
                    print(f"gesture: {event.kind} at {int(event.at[0])},{int(event.at[1])}")
                if gestures.holding and gestures.anchor is not None and not gestures.dragging:
                    # Freeze the cursor while pinching so the click lands where
                    # the user aimed, not where their eye drifted mid-gesture.
                    frozen = True
                    gaze_point = gestures.anchor
                flash = gestures.recent_event()

            # ---------------- output ----------------
            if gaze_point is not None:
                if mouse_enabled and not frozen:
                    mouse.move(*gaze_point)
                color = AMBER if frozen else (GREEN if not drift_warning else CYAN)
                status = "Head moved - press R to fix drift" if drift_warning else ""
                overlay.show_bubble(
                    gaze_point[0], gaze_point[1], bubble_enabled, status,
                    color=color, frozen=frozen, flash=flash,
                )
            else:
                overlay.show_bubble(
                    float(bubble[0]), float(bubble[1]), False,
                    "Eyes not visible" if mapper.ready else "Press C to calibrate",
                )
            overlay.update()

            window_created = _pump_preview(
                preview_visible, frame, usable, hand_landmarks, gestures, mapper.ready,
                False, mouse_enabled, fps, accuracy_text, drift_warning, window_created,
            )

            # ---------------- keys ----------------
            actions = keys.poll(cv2.waitKey(1) & 0xFF)
            if "quit" in actions:
                break
            if "calibrate" in actions:
                mapper.models = []
                mapper.affine = None
                feature_history.clear()
                smoother.reset()
                calibration = Calibration(full_targets, mode="full")
                calibration.start()
            if "drift" in actions and mapper.ready:
                calibration = Calibration(drift_targets, mode="drift", settle=0.45, sample=0.6)
                calibration.start()
            if "validate" in actions and mapper.ready:
                calibration = Calibration(check_targets, mode="validate", settle=0.5, sample=0.7)
                calibration.start()
            if "bubble" in actions:
                bubble_enabled = not bubble_enabled
            if "preview" in actions:
                preview_visible = not preview_visible
            if "mouse" in actions:
                mouse_enabled = not mouse_enabled and mouse.backend != "none"
                if not mouse_enabled and gestures and gestures.dragging:
                    mouse.release("left")
            if "gestures" in actions and gestures:
                gestures_enabled = not gestures_enabled
            if "save" in actions and mapper.ready:
                CALIBRATION_FILE.write_text(
                    json.dumps(mapper.to_dict(overlay.width, overlay.height))
                )
                print(f"Saved calibration to {CALIBRATION_FILE}")
            if "load" in actions and CALIBRATION_FILE.exists():
                try:
                    payload = json.loads(CALIBRATION_FILE.read_text())
                    if mapper.load_dict(payload, overlay.width, overlay.height):
                        smoother.reset()
                        print("Calibration loaded.")
                except (OSError, ValueError, KeyError):
                    print("Could not load the saved calibration.")

            if window_created and cv2.getWindowProperty(APP_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        if gestures and gestures.dragging:
            mouse.release("left")
        camera.release()
        landmarker.close()
        if hands:
            hands.close()
        overlay.close()
        cv2.destroyAllWindows()


def _pump_preview(visible: bool, frame, reading, hand, gestures, calibrated: bool,
                  calibrating: bool, mouse_on: bool, fps: float, accuracy: str,
                  drift_warning: bool, window_created: bool) -> bool:
    if visible:
        preview = draw_preview(
            frame, reading, hand, gestures, calibrated, calibrating,
            mouse_on, fps, accuracy, drift_warning,
        )
        if not window_created:
            cv2.namedWindow(APP_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(APP_NAME, 640, 360)
        cv2.imshow(APP_NAME, preview)
        return True
    if window_created:
        cv2.destroyWindow(APP_NAME)
    return False


if __name__ == "__main__":
    try:
        run()
    except (RuntimeError, ValueError, tk.TclError) as error:
        print(f"\n{APP_NAME}: {error}")
        raise SystemExit(1) from error