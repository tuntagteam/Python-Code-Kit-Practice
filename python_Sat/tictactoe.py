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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x , y = pygame.mouse.get_pos()

            col = x // 200
            row = y // 200
            if board[row][col] == "":
                board[row][col] = current_player

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

    pygame.display.update()
pygame.quit()