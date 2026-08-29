import curses
import random
import time


WIDTH = 60
HEIGHT = 22

BIRD_X = 12
GRAVITY = 0.35
FLAP_STRENGTH = -2.2
PIPE_SPEED = 1
PIPE_GAP = 6
PIPE_WIDTH = 3
PIPE_DISTANCE = 18
FRAME_DELAY = 0.06


def draw_centered(stdscr, y, text):
    h, w = stdscr.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    try:
        stdscr.addstr(y, x, text)
    except curses.error:
        pass


def wait_for_start(stdscr):
    stdscr.clear()

    draw_centered(stdscr, 4, "======================================")
    draw_centered(stdscr, 6, "        FLAPPY TERMINAL BIRD")
    draw_centered(stdscr, 8, "======================================")
    draw_centered(stdscr, 11, "SPACE = FLAP")
    draw_centered(stdscr, 12, "Q     = QUIT")
    draw_centered(stdscr, 15, "Press SPACE to start")

    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == ord("q"):
            return False

        if key == ord(" "):
            return True

        time.sleep(0.03)


def game_over_screen(stdscr, score):
    stdscr.nodelay(False)
    stdscr.clear()

    draw_centered(stdscr, 6, "GAME OVER")
    draw_centered(stdscr, 8, f"SCORE: {score}")
    draw_centered(stdscr, 11, "SPACE = PLAY AGAIN")
    draw_centered(stdscr, 12, "Q     = QUIT")

    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == ord("q"):
            return False

        if key == ord(" "):
            return True


def create_pipe(x):
    top_height = random.randint(3, HEIGHT - PIPE_GAP - 5)

    return {
        "x": x,
        "top": top_height,
        "passed": False
    }


def collision(bird_y, pipes):
    bird_row = int(round(bird_y))

    if bird_row <= 1:
        return True

    if bird_row >= HEIGHT - 2:
        return True

    for pipe in pipes:
        pipe_x = int(pipe["x"])

        if pipe_x <= BIRD_X <= pipe_x + PIPE_WIDTH - 1:
            gap_start = pipe["top"]
            gap_end = gap_start + PIPE_GAP

            if bird_row < gap_start or bird_row >= gap_end:
                return True

    return False


def draw_game(stdscr, bird_y, pipes, score):
    stdscr.erase()

    terminal_h, terminal_w = stdscr.getmaxyx()

    offset_x = max(0, (terminal_w - WIDTH) // 2)
    offset_y = max(0, (terminal_h - HEIGHT) // 2)

    # border
    for x in range(WIDTH):
        try:
            stdscr.addch(offset_y, offset_x + x, "=")
            stdscr.addch(offset_y + HEIGHT - 1, offset_x + x, "=")
        except curses.error:
            pass

    for y in range(1, HEIGHT - 1):
        try:
            stdscr.addch(offset_y + y, offset_x, "|")
            stdscr.addch(offset_y + y, offset_x + WIDTH - 1, "|")
        except curses.error:
            pass

    # score
    score_text = f"SCORE: {score}"

    try:
        stdscr.addstr(
            offset_y,
            offset_x + WIDTH - len(score_text) - 2,
            score_text
        )
    except curses.error:
        pass

    # pipes
    for pipe in pipes:
        px = int(pipe["x"])
        top = pipe["top"]
        gap_end = top + PIPE_GAP

        for x in range(px, px + PIPE_WIDTH):
            if x <= 0 or x >= WIDTH - 1:
                continue

            for y in range(1, top):
                try:
                    stdscr.addch(
                        offset_y + y,
                        offset_x + x,
                        "#"
                    )
                except curses.error:
                    pass

            for y in range(gap_end, HEIGHT - 1):
                try:
                    stdscr.addch(
                        offset_y + y,
                        offset_x + x,
                        "#"
                    )
                except curses.error:
                    pass

    # bird
    bird_row = int(round(bird_y))

    bird_sprite = ">o"

    try:
        stdscr.addstr(
            offset_y + bird_row,
            offset_x + BIRD_X,
            bird_sprite
        )
    except curses.error:
        pass

    # instructions
    instruction = "SPACE = FLAP   Q = QUIT"

    try:
        stdscr.addstr(
            offset_y + HEIGHT,
            offset_x + (WIDTH - len(instruction)) // 2,
            instruction
        )
    except curses.error:
        pass

    stdscr.refresh()


def play_game(stdscr):
    bird_y = HEIGHT // 2
    bird_velocity = 0

    pipes = [
        create_pipe(WIDTH - 5),
        create_pipe(WIDTH - 5 + PIPE_DISTANCE),
        create_pipe(WIDTH - 5 + PIPE_DISTANCE * 2),
    ]

    score = 0

    stdscr.nodelay(True)

    while True:
        start_time = time.time()

        # -------------------------
        # INPUT
        # -------------------------

        key = stdscr.getch()

        if key == ord("q"):
            return None

        if key == ord(" "):
            bird_velocity = FLAP_STRENGTH

        # -------------------------
        # BIRD PHYSICS
        # -------------------------

        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # -------------------------
        # MOVE PIPES
        # -------------------------

        for pipe in pipes:
            pipe["x"] -= PIPE_SPEED

        # -------------------------
        # SCORE
        # -------------------------

        for pipe in pipes:
            if not pipe["passed"] and pipe["x"] + PIPE_WIDTH < BIRD_X:
                pipe["passed"] = True
                score += 1

        # -------------------------
        # REMOVE / CREATE PIPES
        # -------------------------

        if pipes and pipes[0]["x"] + PIPE_WIDTH < 0:
            pipes.pop(0)

            last_x = pipes[-1]["x"]

            pipes.append(
                create_pipe(last_x + PIPE_DISTANCE)
            )

        # -------------------------
        # COLLISION
        # -------------------------

        if collision(bird_y, pipes):
            draw_game(stdscr, bird_y, pipes, score)
            time.sleep(0.5)
            return score

        # -------------------------
        # DRAW
        # -------------------------

        draw_game(
            stdscr,
            bird_y,
            pipes,
            score
        )

        # -------------------------
        # FRAME RATE
        # -------------------------

        elapsed = time.time() - start_time
        sleep_time = FRAME_DELAY - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)


def main(stdscr):
    curses.curs_set(0)

    stdscr.keypad(True)

    while True:

        if not wait_for_start(stdscr):
            break

        score = play_game(stdscr)

        if score is None:
            break

        if not game_over_screen(stdscr, score):
            break


if __name__ == "__main__":
    curses.wrapper(main)