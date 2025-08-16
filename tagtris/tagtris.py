import pygame
import random
import math
import json
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 25
BOARD_X = 350
BOARD_Y = 50

# Enhanced Color Palette
COLORS = {
    'background': (15, 15, 25),
    'board_bg': (25, 25, 40),
    'grid': (40, 40, 60),
    'text_primary': (255, 255, 255),
    'text_secondary': (180, 180, 200),
    'accent': (100, 200, 255),
    'success': (100, 255, 150),
    'warning': (255, 200, 100),
    'danger': (255, 100, 100),
    'panel_bg': (30, 30, 50),
    'panel_border': (60, 60, 100),
}

# Tetromino colors with gradients
TETROMINO_COLORS = [
    None,  # Empty
    (0, 255, 255),   # I - Cyan
    (0, 100, 255),   # J - Blue  
    (255, 165, 0),   # L - Orange
    (255, 255, 0),   # O - Yellow
    (0, 255, 0),     # S - Green
    (255, 0, 0),     # Z - Red
    (160, 0, 255)    # T - Purple
]

# Tetromino shapes
TETROMINOES = [
    [['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..']],  # I
    
    [['.....',
      '.....',
      '.##..',
      '.#...',
      '.#...'],
     ['.....',
      '.....',
      '.#...',
      '.###.',
      '.....']],  # J
    
    [['.....',
      '.....',
      '.##..',
      '..#..',
      '..#..'],
     ['.....',
      '.....',
      '.....',
      '.###.',
      '.#...']],  # L
    
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],  # O
    
    [['.....',
      '.....',
      '..##.',
      '.##..',
      '.....'],
     ['.....',
      '.....',
      '.#...',
      '.##..',
      '..#..']],  # S
    
    [['.....',
      '.....',
      '.##..',
      '..##.',
      '.....'],
     ['.....',
      '.....',
      '..#..',
      '.##..',
      '.#...']],  # Z
    
    [['.....',
      '.....',
      '.###.',
      '..#..',
      '.....'],
     ['.....',
      '.....',
      '..#..',
      '.##..',
      '..#..'],
     ['.....',
      '.....',
      '..#..',
      '.###.',
      '.....'],
     ['.....',
      '.....',
      '.#...',
      '.##..',
      '.#...']]   # T
]

class Particle:
    def __init__(self, x, y, color, velocity, life):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.life = life
        self.max_life = life
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity[1] += 0.2  # gravity
        self.life -= 1
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha)
            pygame.draw.circle(screen, self.color[:3], (int(self.x), int(self.y)), 3)

class GameStats:
    def __init__(self):
        self.load_stats()
        
    def load_stats(self):
        try:
            with open("tetris_stats.json", "r") as f:
                data = json.load(f)
                self.high_score = data.get("high_score", 0)
                self.total_lines = data.get("total_lines", 0)
                self.total_games = data.get("total_games", 0)
        except:
            self.high_score = 0
            self.total_lines = 0
            self.total_games = 0
            
    def save_stats(self):
        data = {
            "high_score": self.high_score,
            "total_lines": self.total_lines,
            "total_games": self.total_games
        }
        with open("tetris_stats.json", "w") as f:
            json.dump(data, f)
            
    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            self.save_stats()
            return True
        return False

class Tetromino:
    def __init__(self, x, y, shape_type=None):
        self.x = x
        self.y = y
        self.shape_type = shape_type if shape_type is not None else random.randint(0, len(TETROMINOES) - 1)
        self.rotation = 0
        self.color = TETROMINO_COLORS[self.shape_type + 1]
        
        # Animation properties
        self.drop_time = 0
        self.move_animation = 0
        self.rotation_animation = 0
        
    def get_shape(self):
        return TETROMINOES[self.shape_type][self.rotation % len(TETROMINOES[self.shape_type])]
        
    def get_cells(self):
        shape = self.get_shape()
        cells = []
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    cells.append((self.x + j, self.y + i))
        return cells
        
    def rotate(self):
        self.rotation += 1
        self.rotation_animation = 10  # Animation frames
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if dx != 0:
            self.move_animation = 5  # Animation frames

class TetrisGame:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_pieces = [Tetromino(0, 0) for _ in range(3)]
        self.held_piece = None
        self.can_hold = True
        
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        
        self.game_state = "playing"  # playing, paused, game_over, menu
        self.particles = []
        self.line_clear_animation = []
        self.combo = 0
        self.back_to_back = False
        
        self.stats = GameStats()
        
        # UI Animation
        self.ui_animations = {
            'score_pulse': 0,
            'level_pulse': 0,
            'line_flash': 0
        }
        
        self.spawn_piece()
        
    def spawn_piece(self):
        self.current_piece = self.next_pieces.pop(0)
        self.current_piece.x = BOARD_WIDTH // 2 - 2
        self.current_piece.y = 0
        self.next_pieces.append(Tetromino(0, 0))
        self.can_hold = True

        # Only trigger game over if the spawn cells overlap existing blocks
        if any((y >= 0 and self.board[y][x] != 0) for x, y in self.current_piece.get_cells()):
            # Prevent immediate game over after a valid hard drop
            if not any(y < 0 for x, y in self.current_piece.get_cells()):
                self.game_state = "game_over"
                self.stats.total_games += 1
                if self.stats.update_high_score(self.score):
                    # New high score animation
                    self.ui_animations['score_pulse'] = 30
                
    def check_collision(self, piece, dx=0, dy=0):
        for x, y in piece.get_cells():
            new_x, new_y = x + dx, y + dy
            if (new_x < 0 or new_x >= BOARD_WIDTH or 
                new_y >= BOARD_HEIGHT or 
                (new_y >= 0 and self.board[new_y][new_x] != 0)):
                return True
        return False
        
    def place_piece(self):
        cells = self.current_piece.get_cells()
        for x, y in cells:
            if y >= 0:
                self.board[y][x] = self.current_piece.shape_type + 1
                
        # Particle effects
        for x, y in cells:
            if y >= 0:
                for _ in range(3):
                    px = BOARD_X + x * BLOCK_SIZE + BLOCK_SIZE // 2
                    py = BOARD_Y + y * BLOCK_SIZE + BLOCK_SIZE // 2
                    velocity = (random.uniform(-2, 2), random.uniform(-3, -1))
                    self.particles.append(Particle(px, py, self.current_piece.color, velocity, 30))
                    
        lines_cleared = self.clear_lines()
        self.update_score(lines_cleared)
        self.spawn_piece()
        
    def clear_lines(self):
        lines_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all(self.board[y][x] != 0 for x in range(BOARD_WIDTH)):
                lines_to_clear.append(y)
                
        if lines_to_clear:
            # Line clear animation
            self.line_clear_animation = [(y, 20) for y in lines_to_clear]
            self.ui_animations['line_flash'] = 20
            
            # Create explosion particles
            for y in lines_to_clear:
                for x in range(BOARD_WIDTH):
                    px = BOARD_X + x * BLOCK_SIZE + BLOCK_SIZE // 2
                    py = BOARD_Y + y * BLOCK_SIZE + BLOCK_SIZE // 2
                    for _ in range(5):
                        velocity = (random.uniform(-4, 4), random.uniform(-4, 4))
                        color = TETROMINO_COLORS[self.board[y][x]] if self.board[y][x] != 0 else (255, 255, 255)
                        self.particles.append(Particle(px, py, color, velocity, 40))
                        
            # Remove cleared lines
            for y in sorted(lines_to_clear, reverse=True):
                del self.board[y]
                self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
                
        return len(lines_to_clear)
        
    def update_score(self, lines_cleared):
        if lines_cleared > 0:
            # Scoring system
            base_score = [0, 100, 300, 500, 800][lines_cleared]
            score_multiplier = self.level
            
            # Combo bonus
            if self.combo > 0:
                base_score += 50 * self.combo * self.level
                
            # Back-to-back bonus
            if lines_cleared == 4:  # Tetris
                if self.back_to_back:
                    base_score = int(base_score * 1.5)
                self.back_to_back = True
            else:
                self.back_to_back = False
                
            self.score += base_score * score_multiplier
            self.lines_cleared += lines_cleared
            self.combo += 1
            
            # Level progression
            new_level = min(20, 1 + self.lines_cleared // 10)
            if new_level > self.level:
                self.level = new_level
                self.fall_speed = max(50, 500 - (self.level - 1) * 25)
                self.ui_animations['level_pulse'] = 20
                
            self.ui_animations['score_pulse'] = 15
            self.stats.total_lines += lines_cleared
        else:
            self.combo = 0
            
    def hold_piece(self):
        if not self.can_hold:
            return
            
        if self.held_piece is None:
            self.held_piece = self.current_piece.shape_type
            self.spawn_piece()
        else:
            # Swap current and held pieces
            temp = self.held_piece
            self.held_piece = self.current_piece.shape_type
            self.current_piece = Tetromino(BOARD_WIDTH // 2 - 2, 0, temp)
            
        self.can_hold = False
        
    def move_piece(self, dx, dy):
        if self.current_piece and not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        return False
        
    def rotate_piece(self):
        if self.current_piece:
            original_rotation = self.current_piece.rotation
            self.current_piece.rotate()
            
            # Wall kick system
            kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
            for dx, dy in kicks:
                if not self.check_collision(self.current_piece, dx, dy):
                    self.current_piece.move(dx, dy)
                    return
                    
            # Rotation failed, revert
            self.current_piece.rotation = original_rotation
            
    def hard_drop(self):
        if self.current_piece:
            drop_distance = 0
            while not self.check_collision(self.current_piece, 0, 1):
                self.current_piece.move(0, 1)
                drop_distance += 1
                
            self.score += drop_distance * 2  # Hard drop bonus
            self.place_piece()
            
    def get_ghost_y(self):
        if not self.current_piece:
            return 0
            
        ghost_y = self.current_piece.y
        while not self.check_collision(self.current_piece, 0, ghost_y - self.current_piece.y + 1):
            ghost_y += 1
        return ghost_y
        
    def update(self, dt):
        # Update animations
        for key in self.ui_animations:
            if self.ui_animations[key] > 0:
                self.ui_animations[key] -= 1
                
        # Update line clear animation
        self.line_clear_animation = [(y, frames - 1) for y, frames in self.line_clear_animation if frames > 1]
        
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()
            
        # Update piece animations
        if self.current_piece:
            if self.current_piece.move_animation > 0:
                self.current_piece.move_animation -= 1
            if self.current_piece.rotation_animation > 0:
                self.current_piece.rotation_animation -= 1
                
        # Piece falling
        if self.game_state == "playing" and self.current_piece:
            self.fall_time += dt
            if self.fall_time >= self.fall_speed:
                if not self.move_piece(0, 1):
                    self.place_piece()
                self.fall_time = 0

def draw_gradient_rect(screen, color1, color2, rect):
    """Draw a rectangle with vertical gradient"""
    for y in range(rect.height):
        ratio = y / rect.height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (r, g, b), 
                        (rect.x, rect.y + y), 
                        (rect.x + rect.width, rect.y + y))

def draw_block(screen, x, y, color, size=BLOCK_SIZE, glow=False):
    """Draw a tetromino block with gradient and glow effects"""
    rect = pygame.Rect(x, y, size, size)
    
    # Create gradient colors
    light_color = tuple(min(255, c + 40) for c in color)
    dark_color = tuple(max(0, c - 40) for c in color)
    
    # Draw glow effect
    if glow:
        glow_rect = pygame.Rect(x - 2, y - 2, size + 4, size + 4)
        glow_color = tuple(min(255, c + 60) for c in color)
        pygame.draw.rect(screen, glow_color, glow_rect, border_radius=3)
    
    # Draw main block with gradient
    draw_gradient_rect(screen, light_color, dark_color, rect)
    
    # Draw border
    pygame.draw.rect(screen, tuple(max(0, c - 60) for c in color), rect, 2, border_radius=2)
    
    # Draw highlight
    highlight_rect = pygame.Rect(x + 2, y + 2, size - 4, size // 3)
    highlight_color = tuple(min(255, c + 80) for c in light_color)
    pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=1)

def draw_tetromino(screen, tetromino, offset_x=0, offset_y=0, ghost=False, small=False):
    """Draw a tetromino piece"""
    if not tetromino:
        return
        
    shape = tetromino.get_shape()
    block_size = BLOCK_SIZE // 2 if small else BLOCK_SIZE
    
    # Animation offset
    anim_offset_x = 0
    anim_offset_y = 0
    
    if hasattr(tetromino, 'move_animation') and tetromino.move_animation > 0:
        anim_offset_x = math.sin(tetromino.move_animation * 0.5) * 2
        
    if hasattr(tetromino, 'rotation_animation') and tetromino.rotation_animation > 0:
        angle = tetromino.rotation_animation * 0.3
        anim_offset_x += math.sin(angle) * 1
        anim_offset_y += math.cos(angle) * 1
    
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == '#':
                x = offset_x + (tetromino.x + j) * block_size + anim_offset_x
                y = offset_y + (tetromino.y + i) * block_size + anim_offset_y
                
                if ghost:
                    # Draw ghost piece (semi-transparent)
                    ghost_color = tuple(c // 3 for c in tetromino.color)
                    pygame.draw.rect(screen, ghost_color, 
                                   (x, y, block_size, block_size), 2, border_radius=2)
                else:
                    draw_block(screen, x, y, tetromino.color, block_size)

def draw_board(screen, game):
    """Draw the game board"""
    # Board background
    board_rect = pygame.Rect(BOARD_X - 5, BOARD_Y - 5, 
                           BOARD_WIDTH * BLOCK_SIZE + 10, 
                           BOARD_HEIGHT * BLOCK_SIZE + 10)
    draw_gradient_rect(screen, COLORS['board_bg'], 
                      tuple(max(0, c - 10) for c in COLORS['board_bg']), board_rect)
    pygame.draw.rect(screen, COLORS['panel_border'], board_rect, 2, border_radius=5)
    
    # Grid lines
    for x in range(BOARD_WIDTH + 1):
        pygame.draw.line(screen, COLORS['grid'], 
                        (BOARD_X + x * BLOCK_SIZE, BOARD_Y),
                        (BOARD_X + x * BLOCK_SIZE, BOARD_Y + BOARD_HEIGHT * BLOCK_SIZE))
    for y in range(BOARD_HEIGHT + 1):
        pygame.draw.line(screen, COLORS['grid'],
                        (BOARD_X, BOARD_Y + y * BLOCK_SIZE),
                        (BOARD_X + BOARD_WIDTH * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE))
    
    # Draw placed blocks
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if game.board[y][x] != 0:
                # Check if this line is being cleared
                is_clearing = any(ly == y for ly, _ in game.line_clear_animation)
                glow = is_clearing
                
                block_x = BOARD_X + x * BLOCK_SIZE
                block_y = BOARD_Y + y * BLOCK_SIZE
                color = TETROMINO_COLORS[game.board[y][x]]
                
                if is_clearing:
                    # Flash effect during line clear
                    flash_intensity = max(0, min(255, 100 + game.ui_animations['line_flash'] * 8))
                    color = tuple(min(255, c + flash_intensity) for c in color)
                
                draw_block(screen, block_x, block_y, color, glow=glow)
    
    # Draw ghost piece
    if game.current_piece:
        ghost_piece = Tetromino(0, 0, game.current_piece.shape_type)
        ghost_piece.x = game.current_piece.x
        ghost_piece.y = game.get_ghost_y()
        ghost_piece.rotation = game.current_piece.rotation
        
        if ghost_piece.y != game.current_piece.y:
            draw_tetromino(screen, ghost_piece, BOARD_X, BOARD_Y, ghost=True)
    
    # Draw current piece
    if game.current_piece:
        draw_tetromino(screen, game.current_piece, BOARD_X, BOARD_Y)

def draw_panel(screen, title, x, y, width, height, content=None):
    """Draw a UI panel"""
    # Panel background
    panel_rect = pygame.Rect(x, y, width, height)
    draw_gradient_rect(screen, COLORS['panel_bg'], 
                      tuple(max(0, c - 15) for c in COLORS['panel_bg']), panel_rect)
    pygame.draw.rect(screen, COLORS['panel_border'], panel_rect, 2, border_radius=8)
    
    # Title
    font = pygame.font.Font(None, 24)
    title_surface = font.render(title, True, COLORS['accent'])
    screen.blit(title_surface, (x + 10, y + 10))
    
    return y + 35  # Return y position for content

def draw_ui(screen, game):
    """Draw the user interface"""
    font_large = pygame.font.Font(None, 36)
    font_medium = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24)
    
    # Score panel
    y_pos = draw_panel(screen, "SCORE", 50, 50, 200, 120)
    
    # Score with pulse animation
    score_color = COLORS['text_primary']
    if game.ui_animations['score_pulse'] > 0:
        pulse = game.ui_animations['score_pulse'] / 15.0
        score_color = tuple(min(255, c + int(pulse * 100)) for c in COLORS['success'])
    
    score_text = font_large.render(f"{game.score:,}", True, score_color)
    screen.blit(score_text, (60, y_pos))
    
    high_score_text = font_small.render(f"High: {game.stats.high_score:,}", True, COLORS['text_secondary'])
    screen.blit(high_score_text, (60, y_pos + 40))
    
    # Level panel
    y_pos = draw_panel(screen, "LEVEL", 50, 190, 200, 80)
    
    level_color = COLORS['text_primary']
    if game.ui_animations['level_pulse'] > 0:
        pulse = game.ui_animations['level_pulse'] / 20.0
        level_color = tuple(min(255, c + int(pulse * 120)) for c in COLORS['warning'])
    
    level_text = font_large.render(str(game.level), True, level_color)
    screen.blit(level_text, (60, y_pos))
    
    # Lines panel
    y_pos = draw_panel(screen, "LINES", 50, 290, 200, 80)
    lines_text = font_medium.render(str(game.lines_cleared), True, COLORS['text_primary'])
    screen.blit(lines_text, (60, y_pos))
    
    # Hold panel
    y_pos = draw_panel(screen, "HOLD", 50, 390, 120, 120)
    if game.held_piece is not None:
        held_tetromino = Tetromino(0, 0, game.held_piece)
        # Center the piece in the panel
        draw_tetromino(screen, held_tetromino, 60, y_pos + 10, small=True)
    
    # Next pieces panel
    y_pos = draw_panel(screen, "NEXT", 700, 50, 150, 300)
    for i, next_piece in enumerate(game.next_pieces):
        piece_y = y_pos + i * 80
        draw_tetromino(screen, next_piece, 710, piece_y, small=True)
    
    # Game state overlays
    if game.game_state == "paused":
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("PAUSED", True, COLORS['text_primary'])
        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(pause_text, text_rect)
        
        instruction_text = font_medium.render("Press P to resume", True, COLORS['text_secondary'])
        inst_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        screen.blit(instruction_text, inst_rect)
    
    elif game.game_state == "game_over":
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, COLORS['danger'])
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        screen.blit(game_over_text, text_rect)
        
        final_score_text = font_large.render(f"Final Score: {game.score:,}", True, COLORS['text_primary'])
        score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        screen.blit(final_score_text, score_rect)
        
        if game.score == game.stats.high_score and game.score > 0:
            new_high_text = font_medium.render("NEW HIGH SCORE!", True, COLORS['success'])
            high_rect = new_high_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            screen.blit(new_high_text, high_rect)
        
        restart_text = font_medium.render("Press R to restart", True, COLORS['text_secondary'])
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        screen.blit(restart_text, restart_rect)

def draw_particles(screen, particles):
    """Draw particle effects"""
    for particle in particles:
        particle.draw(screen)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Enhanced Tetris")
    clock = pygame.time.Clock()
    
    game = TetrisGame()
    
    # Input handling
    keys_pressed = set()
    key_repeat_time = {}
    
    running = True
    while running:
        dt = clock.tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                keys_pressed.add(event.key)
                key_repeat_time[event.key] = 0
                
                if game.game_state == "playing":
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                    elif event.key == pygame.K_c:
                        game.hold_piece()
                    # Removed K_x binding for hard drop
                    elif event.key == pygame.K_p:
                        game.game_state = "paused"
                        
                elif game.game_state == "paused":
                    if event.key == pygame.K_p:
                        game.game_state = "playing"
                        
                elif game.game_state == "game_over":
                    if event.key == pygame.K_r:
                        game = TetrisGame()
                        
            elif event.type == pygame.KEYUP:
                keys_pressed.discard(event.key)
                if event.key in key_repeat_time:
                    del key_repeat_time[event.key]
        
        # Handle key repeats
        for key in list(key_repeat_time.keys()):
            key_repeat_time[key] += dt
            if key_repeat_time[key] > 150:  # Initial delay
                if key_repeat_time[key] % 50 < dt:  # Repeat rate
                    if game.game_state == "playing":
                        if key == pygame.K_LEFT:
                            game.move_piece(-1, 0)
                        elif key == pygame.K_RIGHT:
                            game.move_piece(1, 0)
                        elif key == pygame.K_DOWN:
                            game.move_piece(0, 1)
        
        # Update game
        if game.game_state == "playing":
            game.update(dt)
        
        # Draw everything
        screen.fill(COLORS['background'])
        
        # Draw animated background
        for i in range(0, WINDOW_WIDTH, 50):
            for j in range(0, WINDOW_HEIGHT, 50):
                alpha = int(20 + 10 * math.sin((i + j + pygame.time.get_ticks() * 0.001) * 0.01))
                color = tuple(min(255, c + alpha) for c in COLORS['background'])
                pygame.draw.circle(screen, color, (i, j), 2)
        
        draw_board(screen, game)
        draw_ui(screen, game)
        draw_particles(screen, game.particles)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()