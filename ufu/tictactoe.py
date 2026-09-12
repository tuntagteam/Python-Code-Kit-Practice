import pygame

pygame.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Tic Tac Toe")

board = [
    ["","",""],
    ["","",""],
    ["","",""]
]

current_player = "X"
font = pygame.font.SysFont(None, 120)
small_font = pygame.font.SysFont(None,45)

def check_winner():
    for row in range(3):
        if board[row][0] != "" and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]
        
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                return False
    return True

running = True
winner = None
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                board = [
                    ["","",""],
                    ["","",""],
                    ["","",""]
                ]
                current_player = "X"
                winner = None
                game_over = False

        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_over == False:
            x , y = pygame.mouse.get_pos()

            col = x // 200
            row = y // 200
            if board[row][col] == "":
                board[row][col] = current_player
                winner = check_winner()
                if winner != None:
                    game_over = True
                elif check_draw() == True:
                    game_over = True
                else:
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
        
    screen.fill((255,255,255))
    pygame.draw.line(screen, (0,0,0),(200,0) , (200,600) ,5)
    pygame.draw.line(screen, (0,0,0),(400,0),(400,600),5)
    pygame.draw.line(screen, (0, 0, 0), (0, 200), (600, 200), 5)
    pygame.draw.line(screen, (0, 0, 0), (0, 400), (600, 400), 5)

    for row in range(3):
        for col in range(3):
            mark = board[row][col]

            if mark != "":
                text = font.render(mark, True, (0,0,0))
                screen.blit(text, (col*200+70, row*200+45))

    if game_over == True:
        if winner != None:
            message = small_font.render(winner + " wins!", True, (255,0,0))
        else:
            message = small_font.render("Tied!!!!!!", True, (255,0,0))
        restart = small_font.render("Press R to restart", True, (0,0,0))

        screen.blit(message, (230,260))
        screen.blit(restart, (170,310))

    pygame.display.update()
pygame.quit()


### ขีดเส้นตอนชนะ / ทำให้สวยขึ้น / เอไอ