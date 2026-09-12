import cv2
import mediapipe as mp
import math
import time
from datetime import datetime
from pathlib import Path


# =========================================================
# CONFIG
# =========================================================

TARGET_COUNT = 67

MOVE_THRESHOLD = 0.025
RESET_THRESHOLD = 0.010

MIN_TIME_BETWEEN_COUNTS = 0.35

WINDOW_NAME = "AI 67 Movement Tracker"

OUTPUT_FILE = Path(__file__).with_name(
    "67_movement_statistics.txt"
)


# =========================================================
# MEDIAPIPE
# =========================================================

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.55,
    min_tracking_confidence=0.55,
)


# =========================================================
# VARIABLES
# =========================================================

counter = 0

previous_center = None

ready = True

last_count_time = 0

movement_strength = 0

movement_log = []

start_time = time.time()

start_datetime = datetime.now()

completed = False

saved = False

fps = 0

previous_frame_time = time.time()


# =========================================================
# FUNCTIONS
# =========================================================

def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )


def get_body_center(landmarks):

    ids = [
        mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
        mp_pose.PoseLandmark.LEFT_HIP.value,
        mp_pose.PoseLandmark.RIGHT_HIP.value,
    ]

    x = sum(
        landmarks[i].x for i in ids
    ) / len(ids)

    y = sum(
        landmarks[i].y for i in ids
    ) / len(ids)

    return x, y


def save_statistics():

    end_datetime = datetime.now()

    duration = time.time() - start_time

    movements_per_minute = (
        counter / duration * 60
        if duration > 0
        else 0
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "========================================\n"
        )

        file.write(
            "       AI 67 MOVEMENT STATISTICS\n"
        )

        file.write(
            "========================================\n\n"
        )

        file.write(
            f"Date        : "
            f"{start_datetime.strftime('%Y-%m-%d')}\n"
        )

        file.write(
            f"Start Time  : "
            f"{start_datetime.strftime('%H:%M:%S')}\n"
        )

        file.write(
            f"End Time    : "
            f"{end_datetime.strftime('%H:%M:%S')}\n"
        )

        file.write(
            f"Target      : {TARGET_COUNT}\n"
        )

        file.write(
            f"Total Moves : {counter}\n"
        )

        file.write(
            f"Duration    : {duration:.2f} seconds\n"
        )

        file.write(
            f"Speed       : "
            f"{movements_per_minute:.2f} moves/min\n"
        )

        file.write("\n")

        if counter >= TARGET_COUNT:
            file.write(
                "Status      : COMPLETED\n"
            )
        else:
            file.write(
                "Status      : STOPPED EARLY\n"
            )

        file.write(
            "\n========================================\n"
        )

        file.write(
            "MOVEMENT LOG\n"
        )

        file.write(
            "========================================\n"
        )

        for number, timestamp in movement_log:

            file.write(
                f"{number:02d} | {timestamp}\n"
            )


def draw_rounded_panel(
    frame,
    x1,
    y1,
    x2,
    y2,
    color
):

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        -1
    )


def draw_pose(
    frame,
    landmarks
):

    h, w = frame.shape[:2]

    connections = mp_pose.POSE_CONNECTIONS

    # Skeleton lines
    for connection in connections:

        start_idx, end_idx = connection

        a = landmarks[start_idx]
        b = landmarks[end_idx]

        if (
            a.visibility > 0.4
            and b.visibility > 0.4
        ):

            x1 = int(a.x * w)
            y1 = int(a.y * h)

            x2 = int(b.x * w)
            y2 = int(b.y * h)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 170, 30),
                3,
                cv2.LINE_AA
            )

    # AI tracking points
    for lm in landmarks:

        if lm.visibility > 0.5:

            x = int(lm.x * w)
            y = int(lm.y * h)

            cv2.circle(
                frame,
                (x, y),
                7,
                (50, 220, 255),
                -1
            )

            cv2.circle(
                frame,
                (x, y),
                3,
                (255, 255, 255),
                -1
            )


def draw_progress_bar(
    frame,
    x,
    y,
    width,
    height,
    progress
):

    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (60, 65, 75),
        -1
    )

    fill_width = int(
        width * progress
    )

    if fill_width > 0:

        cv2.rectangle(
            frame,
            (x, y),
            (
                x + fill_width,
                y + height
            ),
            (60, 220, 120),
            -1
        )


def reset_counter():

    global counter
    global previous_center
    global ready
    global last_count_time
    global movement_strength
    global movement_log
    global start_time
    global start_datetime
    global completed
    global saved

    counter = 0

    previous_center = None

    ready = True

    last_count_time = 0

    movement_strength = 0

    movement_log = []

    start_time = time.time()

    start_datetime = datetime.now()

    completed = False

    saved = False


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)

camera.set(
    cv2.CAP_PROP_FPS,
    30
)


if not camera.isOpened():

    print("ERROR: Could not open camera.")

    exit()


cv2.namedWindow(
    WINDOW_NAME,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    WINDOW_NAME,
    1280,
    720
)


# =========================================================
# MAIN
# =========================================================

while True:

    success, frame = camera.read()

    if not success:
        break


    # Mirror webcam
    frame = cv2.flip(
        frame,
        1
    )


    h, w = frame.shape[:2]


    # =====================================================
    # FPS
    # =====================================================

    now = time.time()

    delta = (
        now -
        previous_frame_time
    )

    if delta > 0:

        current_fps = (
            1 / delta
        )

        fps = (
            fps * 0.9 +
            current_fps * 0.1
        )

    previous_frame_time = now


    # =====================================================
    # MEDIAPIPE
    # =====================================================

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    rgb.flags.writeable = False

    results = pose.process(
        rgb
    )

    rgb.flags.writeable = True


    person_detected = False


    if results.pose_landmarks:

        person_detected = True

        landmarks = (
            results
            .pose_landmarks
            .landmark
        )


        draw_pose(
            frame,
            landmarks
        )


        center = get_body_center(
            landmarks
        )


        # =================================================
        # MOVEMENT
        # =================================================

        if previous_center:

            raw_movement = distance(
                previous_center,
                center
            )

            movement_strength = (
                movement_strength * 0.70 +
                raw_movement * 0.30
            )


        previous_center = center


        current_time = time.time()


        if (
            movement_strength
            > MOVE_THRESHOLD
        ):

            if (
                ready
                and
                current_time - last_count_time
                >= MIN_TIME_BETWEEN_COUNTS
                and
                not completed
            ):

                counter += 1

                ready = False

                last_count_time = (
                    current_time
                )

                movement_log.append(
                    (
                        counter,
                        datetime.now().strftime(
                            "%H:%M:%S.%f"
                        )[:-3]
                    )
                )

                print(
                    f"Movement #{counter}"
                )


        elif (
            movement_strength
            < RESET_THRESHOLD
        ):

            ready = True


    # =====================================================
    # BACKGROUND UI OVERLAY
    # =====================================================

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (0, 0),
        (420, h),
        (12, 15, 22),
        -1
    )

    frame = cv2.addWeighted(
        overlay,
        0.82,
        frame,
        0.18,
        0
    )


    # =====================================================
    # HEADER
    # =====================================================

    cv2.putText(
        frame,
        "AI MOTION",
        (35, 65),
        cv2.FONT_HERSHEY_DUPLEX,
        1.25,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    cv2.putText(
        frame,
        "TRACKING SYSTEM",
        (35, 98),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (120, 130, 150),
        1,
        cv2.LINE_AA
    )


    # =====================================================
    # STATUS
    # =====================================================

    status_y = 140

    if person_detected:

        cv2.circle(
            frame,
            (45, status_y),
            7,
            (70, 230, 120),
            -1
        )

        status = (
            "BODY DETECTED"
        )

        status_color = (
            100,
            255,
            160
        )

    else:

        cv2.circle(
            frame,
            (45, status_y),
            7,
            (60, 180, 255),
            -1
        )

        status = (
            "SEARCHING..."
        )

        status_color = (
            100,
            200,
            255
        )


    cv2.putText(
        frame,
        status,
        (65, status_y + 7),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        status_color,
        2,
        cv2.LINE_AA
    )


    # =====================================================
    # COUNTER CARD
    # =====================================================

    draw_rounded_panel(
        frame,
        30,
        180,
        390,
        350,
        (25, 30, 42)
    )


    cv2.putText(
        frame,
        "MOVEMENT COUNT",
        (55, 220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (140, 150, 170),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        frame,
        str(counter),
        (50, 310),
        cv2.FONT_HERSHEY_DUPLEX,
        2.7,
        (255, 255, 255),
        4,
        cv2.LINE_AA
    )


    cv2.putText(
        frame,
        f"/ {TARGET_COUNT}",
        (185, 310),
        cv2.FONT_HERSHEY_DUPLEX,
        1.2,
        (130, 140, 160),
        2,
        cv2.LINE_AA
    )


    # =====================================================
    # PROGRESS
    # =====================================================

    progress = min(
        counter / TARGET_COUNT,
        1
    )

    draw_progress_bar(
        frame,
        55,
        325,
        310,
        8,
        progress
    )


    percentage = int(
        progress * 100
    )


    cv2.putText(
        frame,
        f"{percentage}% COMPLETE",
        (55, 375),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (170, 180, 200),
        1,
        cv2.LINE_AA
    )


    # =====================================================
    # MOVEMENT METER
    # =====================================================

    cv2.putText(
        frame,
        "MOTION INTENSITY",
        (35, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.52,
        (140, 150, 170),
        1,
        cv2.LINE_AA
    )


    meter_width = 330

    normalized_motion = min(
        movement_strength / 0.08,
        1
    )

    cv2.rectangle(
        frame,
        (35, 450),
        (35 + meter_width, 470),
        (45, 50, 60),
        -1
    )


    cv2.rectangle(
        frame,
        (35, 450),
        (
            35 +
            int(
                meter_width *
                normalized_motion
            ),
            470
        ),
        (60, 190, 255),
        -1
    )


    # =====================================================
    # STATS
    # =====================================================

    elapsed = (
        time.time() -
        start_time
    )


    cv2.putText(
        frame,
        f"TIME   {elapsed:06.1f}s",
        (35, 525),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (220, 225, 235),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        frame,
        f"FPS    {fps:05.1f}",
        (35, 560),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (220, 225, 235),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        frame,
        f"TARGET {TARGET_COUNT}",
        (35, 595),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (220, 225, 235),
        1,
        cv2.LINE_AA
    )


    # =====================================================
    # KEYBOARD HELP
    # =====================================================

    cv2.putText(
        frame,
        "R   RESET",
        (35, h - 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (120, 130, 150),
        1,
        cv2.LINE_AA
    )


    cv2.putText(
        frame,
        "Q   QUIT + SAVE",
        (35, h - 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (120, 130, 150),
        1,
        cv2.LINE_AA
    )


    # =====================================================
    # COMPLETE
    # =====================================================

    if counter >= TARGET_COUNT:

        completed = True


        if not saved:

            save_statistics()

            saved = True

            print(
                "\nTARGET COMPLETE!"
            )

            print(
                f"Statistics saved:\n"
                f"{OUTPUT_FILE}"
            )


        box_width = 620
        box_height = 170

        x1 = (
            w // 2 -
            box_width // 2 +
            200
        )

        y1 = (
            h // 2 -
            box_height // 2
        )


        cv2.rectangle(
            frame,
            (x1, y1),
            (
                x1 + box_width,
                y1 + box_height
            ),
            (15, 20, 28),
            -1
        )


        cv2.putText(
            frame,
            "TARGET COMPLETE",
            (
                x1 + 80,
                y1 + 65
            ),
            cv2.FONT_HERSHEY_DUPLEX,
            1.35,
            (100, 255, 160),
            3,
            cv2.LINE_AA
        )


        cv2.putText(
            frame,
            "67 movements recorded successfully",
            (
                x1 + 80,
                y1 + 110
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (220, 225, 235),
            1,
            cv2.LINE_AA
        )


        cv2.putText(
            frame,
            "Statistics saved automatically",
            (
                x1 + 80,
                y1 + 140
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (140, 150, 170),
            1,
            cv2.LINE_AA
        )


    # =====================================================
    # DISPLAY
    # =====================================================

    cv2.imshow(
        WINDOW_NAME,
        frame
    )


    key = cv2.waitKey(
        1
    ) & 0xFF


    if key == ord("q"):

        if not saved:
            save_statistics()

        break


    elif key == ord("r"):

        reset_counter()

        print(
            "Counter reset."
        )


# =========================================================
# CLEANUP
# =========================================================

camera.release()

pose.close()

cv2.destroyAllWindows()


print()
print(
    "================================"
)

print(
    "AI Movement Tracker closed"
)

print(
    f"Final count: {counter}"
)

print(
    f"Statistics file:"
)

print(
    OUTPUT_FILE
)

print(
    "================================"
)