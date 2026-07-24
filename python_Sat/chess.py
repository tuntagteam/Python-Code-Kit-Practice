import io
import sys

import pygame

try:
    import python_Sat.chess as chess
    import chess.svg
    import cairosvg
except ImportError as error:
    print("Missing library:", error)
    print("Install with: python3 -m pip install pygame python-chess cairosvg")
    sys.exit()

pygame.init()

WIDTH = 640
BOARD_SIZE = 640
STATUS_HEIGHT = 80
HEIGHT = BOARD_SIZE + STATUS_HEIGHT
SQ = BOARD_SIZE // 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess Game")

font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 30)

board = chess.Board()
selected_square = None
legal_target_squares = []

cached_surface = None
cached_key = None


def square_from_mouse(pos):
    x, y = pos

    if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
        return None

    col = x // SQ
    row = y // SQ

    return chess.square(col, 7 - row)


def get_board_surface():
    global cached_surface, cached_key

    key = (
        board.fen(),
        selected_square,
        tuple(legal_target_squares),
        board.peek() if board.move_stack else None,
    )

    if cached_surface is not None and cached_key == key:
        return cached_surface

    fill = {}

    if selected_square is not None:
        fill[selected_square] = "#f6f669"

    for square in legal_target_squares:
        fill[square] = "#baca44"

    svg_data = chess.svg.board(
        board=board,
        size=BOARD_SIZE,
        lastmove=board.peek() if board.move_stack else None,
        check=board.king(board.turn) if board.is_check() else None,
        fill=fill,
    )

    png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    cached_surface = pygame.image.load(io.BytesIO(png_data)).convert_alpha()
    cached_key = key

    return cached_surface


def render_board():
    screen.blit(get_board_surface(), (0, 0))


def get_status_text():
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        return "Checkmate! " + winner + " wins!"

    if board.is_stalemate():
        return "Draw! Stalemate."

    if board.is_insufficient_material():
        return "Draw! Insufficient material."

    if board.is_seventyfive_moves():
        return "Draw! 75-move rule."

    if board.is_fivefold_repetition():
        return "Draw! Fivefold repetition."

    turn = "White" if board.turn == chess.WHITE else "Black"

    if board.is_check():
        return turn + " is in check!"

    return turn + "'s turn"


def draw_status():
    pygame.draw.rect(screen, (30, 30, 30), (0, BOARD_SIZE, WIDTH, STATUS_HEIGHT))

    label = big_font.render(get_status_text(), True, (255, 255, 255))
    screen.blit(label, (20, BOARD_SIZE + 12))

    help_text = font.render("Click piece -> click square | R = restart | U = undo", True, (210, 210, 210))
    screen.blit(help_text, (20, BOARD_SIZE + 48))


def update_legal_targets(square):
    global legal_target_squares

    legal_target_squares = []

    for move in board.legal_moves:
        if move.from_square == square:
            legal_target_squares.append(move.to_square)


def try_move(start, end):
    move = chess.Move(start, end)
    piece = board.piece_at(start)

    if piece and piece.piece_type == chess.PAWN:
        end_rank = chess.square_rank(end)

        if end_rank == 0 or end_rank == 7:
            move = chess.Move(start, end, promotion=chess.QUEEN)

    if move in board.legal_moves:
        board.push(move)
        return True

    return False


def select_square(square):
    global selected_square

    piece = board.piece_at(square)

    if piece and piece.color == board.turn:
        selected_square = square
        update_legal_targets(square)
    else:
        clear_selection()


def clear_selection():
    global selected_square, legal_target_squares

    selected_square = None
    legal_target_squares = []


def handle_click(pos):
    square = square_from_mouse(pos)

    if square is None:
        return

    if board.is_game_over():
        return

    if selected_square is None:
        select_square(square)
        return

    if try_move(selected_square, square):
        clear_selection()
        return

    select_square(square)


def restart_game():
    board.reset()
    clear_selection()


def undo_move():
    if board.move_stack:
        board.pop()
    clear_selection()


def run_game():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))
        render_board()
        draw_status()

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_u:
                    undo_move()

    pygame.quit()


run_game()