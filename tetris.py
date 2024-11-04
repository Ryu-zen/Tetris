import pygame
import random

# Initialize the game
pygame.font.init()

# Global constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

# Shapes of the Tetriminos
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Texture mapping for each shape
TEXTURE_MAP = {
    0: 'cyan.png',   # I
    1: 'yellow.png', # O
    2: 'purple.png', # T
    3: 'green.png',  # S
    4: 'red.png',    # Z
    5: 'orange.png', # L
    6: 'white.png',   # J
}

class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.texture = self.load_texture(SHAPES.index(shape))  # Load the texture based on shape index
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def load_texture(self, shape_index):
        texture_file = TEXTURE_MAP.get(shape_index)
        if texture_file:
            try:
                texture = pygame.image.load(texture_file)
                return pygame.transform.scale(texture, (BLOCK_SIZE, BLOCK_SIZE))  # Scale to BLOCK_SIZE
            except pygame.error as e:
                print(f"Error loading texture {texture_file}: {e}")
        return None

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        return Piece(random.choice(SHAPES))

    def valid_space(self, shape, offset):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = x + offset[0]
                    grid_y = y + offset[1]
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return False
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return False
        return True

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.texture

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0] * GRID_WIDTH)
        self.score += len(lines_to_clear)

    def drop_piece(self):
        if self.valid_space(self.current_piece.shape, (self .current_piece.x, self.current_piece.y + 1)):
            self.current_piece.y += 1
        else:
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if not self.valid_space(self.current_piece.shape, (self.current_piece.x, self.current_piece.y)):
                self.game_over = True

    def move_piece(self, dx):
        if self.valid_space(self.current_piece.shape, (self.current_piece.x + dx, self.current_piece.y)):
            self.current_piece.x += dx

    def rotate_piece(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if not self.valid_space(self.current_piece.shape, (self.current_piece.x, self.current_piece.y)):
            self.current_piece.shape = original_shape

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                surface.blit(grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE))

def draw_piece(surface, piece, x=0, y=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                surface.blit(piece.texture, ((piece.x + x) * BLOCK_SIZE + x, (piece.y + y) * BLOCK_SIZE + y))

def draw_background(surface):
    try:
        background_image = pygame.image.load('background.png')
        surface.blit(background_image, (0, 0))
    except pygame.error as e:
        print(f"Error loading background image: {e}")

def draw_grid_lines(surface):
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, LIGHT_GRAY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, LIGHT_GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    pygame.draw.rect(surface, WHITE, (x - 2, y - 2, text_surface.get_width() + 4, text_surface.get_height() + 4))
    surface.blit(text_surface, (x, y))

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 72)  # Larger font size for the title
    button_font = pygame.font.Font(None, 36)  # Smaller font size for button text

    background_image = pygame.image.load('main_menu_background.png')
    
    # Adjust button dimensions
    button_width = 150
    button_height = 40
    
    # Adjust Y positions to center the buttons further from the title
    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - 40, button_width, button_height)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 10, button_width, button_height)

    # Title text
    title_text = "Tetris"
    title_surface = font.render(title_text, True, BLACK)
    title_stroke_surface = font.render(title_text, True, WHITE)

    # Calculate title position
    title_x = (SCREEN_WIDTH - title_surface.get_width()) // 2
    title_y = SCREEN_HEIGHT // 4  # Position the title towards the top

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    main()
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return

        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Draw the title with stroke effect
        screen.blit(title_stroke_surface, (title_x - 2, title_y - 2))  # Stroke offset
        screen.blit(title_stroke_surface, (title_x + 2, title_y - 2))  # Stroke offset
        screen.blit(title_stroke_surface, (title_x - 2, title_y + 2))  # Stroke offset
        screen.blit(title_stroke_surface, (title_x + 2, title_y + 2))  # Stroke offset
        screen.blit(title_surface, (title_x, title_y))  # Main title text

        # Draw the buttons
        pygame.draw.rect(screen, WHITE, play_again_button)
        pygame.draw.rect(screen, WHITE , quit_button)
        play_again_text = button_font.render("Play", True, BLACK)
        quit_text = button_font.render("Quit", True, BLACK)
        screen.blit(play_again_text, (play_again_button.x + (button_width - play_again_text.get_width()) // 2, play_again_button.y + (button_height - play_again_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))
        
        pygame.display.flip()
        clock.tick(60)
        
def game_over_screen(score):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over")
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 72)  # Larger font size for the title
    score_font = pygame.font.Font(None, 36)   # Font for the score and buttons

    background_image = pygame.image.load('game_over_background.png')  # Load your game over background image
    
    # Button dimensions
    button_width = 150
    button_height = 40
    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2, button_width, button_height)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + 20, button_width, button_height)

    # Game Over title text
    title_text = "Game Over"
    title_surface = title_font.render(title_text, True, BLACK)
    title_stroke_surface = title_font.render(title_text, True, WHITE)

    # Calculate title position
    title_x = (SCREEN_WIDTH - title_surface.get_width()) // 2
    title_y = SCREEN_HEIGHT // 4  # Position the title towards the top

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    main()
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return

        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Draw the title with stroke effect
        screen.blit(title_stroke_surface, (title_x - 2, title_y - 2))  # Stroke offset
        screen.blit(title_stroke_surface, (title_x + 2, title_y - 2))  # Stroke offset
        screen.blit(title_stroke_surface, (title_x - 2, title_y + 2))  # Stroke offset
        screen.blit(title_stroke_surface, (title_x + 2, title_y + 2))  # Stroke offset
        screen.blit(title_surface, (title_x, title_y))  # Main title text

        # Render the score text with stroke effect
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        score_stroke_text = score_font.render(f"Score: {score}", True, WHITE)
        score_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
        score_y = title_y + 50  # Position score below the title

        # Draw the score with stroke effect
        screen.blit(score_stroke_text, (score_x - 2, score_y - 2))  # Stroke offset
        screen.blit(score_stroke_text, (score_x + 2, score_y - 2))  # Stroke offset
        screen.blit(score_stroke_text, (score_x - 2, score_y + 2))  # Stroke offset
        screen.blit(score_stroke_text, (score_x + 2, score_y + 2))  # Stroke offset
        screen.blit(score_text, (score_x, score_y))  # Main score text

        # Draw the buttons
        pygame.draw.rect(screen, WHITE, play_again_button)
        pygame.draw.rect(screen, WHITE, quit_button)

        # Render the button texts
        play_again_text = score_font.render("Play Again", True, BLACK)
        quit_text = score_font.render("Quit", True, BLACK)
        screen.blit(play_again_text, (play_again_button.x + (button_width - play_again_text.get_width()) // 2, play_again_button.y + (button_height - play_again_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + (button_height - quit_text.get_height()) // 2))

        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    tetris = Tetris()
    last_drop_time = pygame.time.get_ticks()

    while not tetris.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece(-1)
                elif event.key == pygame.K_RIGHT:
                    tetris.move_piece(1)
                elif event.key == pygame.K_DOWN:
                    tetris.drop_piece()
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()

        current_time = pygame.time.get_ticks()
        if current_time - last_drop_time > 500:  # 500ms = 0.5s
            tetris.drop_piece()
            last_drop_time = current_time

        screen.fill(BLACK)
        draw_background(screen)
        draw_grid_lines(screen)
        draw_grid(screen, tetris.grid)
        draw_piece(screen, tetris.current_piece)
        draw_piece(screen, tetris.next_piece, x=SCREEN_WIDTH - 100, y=50)  # Draw next piece in a designated area
        score_text = font.render(f"Score: {tetris.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    # Call the game over screen with the final score
    game_over_screen(tetris.score)

if __name__ == "__main__":
    main_menu()
