from board import Board
import pygame

pygame.init()

# DRAW VARIABLES
win_width = win_height = 500  # before: 462
space_between_sections = 10   # before: 3
width, height = 50, 50
padding = (win_width - width * 9 - space_between_sections * 2) // 2

win = pygame.display.set_mode((win_width, win_height))
game_board = Board()

pygame.display.set_caption("SUPER TIC TAC TOE")

winner = 0
current_player_id = 1

run = True
while run:

    pygame.time.delay(300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                i, j, k, l = (event.pos[1] - padding) // (space_between_sections + height * 3),\
                             (event.pos[0] - padding) // (space_between_sections + width * 3),\
                             (event.pos[1] - padding) % (space_between_sections + 3 * height) // height,\
                             (event.pos[0] - padding) % (space_between_sections + 3 * width) // width
                print(i, j, k, l)

                if game_board.mark(game_board.state, current_player_id, i, j, k, l):
                    current_player_id = current_player_id % 2 + 1

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if game_board.state[j][i].state[l][k] == 0:
                        color = (255, 0, 0)
                    elif game_board.state[j][i].state[l][k] == 1:
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    pygame.draw.rect(win, (0, 0, 0), (padding + i * (width * 3 + space_between_sections) + k * width,
                                                      padding + j * (height * 3 + space_between_sections) + l * height,
                                                      width, height))
                    pygame.draw.rect(win, color, (padding + i * (width * 3 + space_between_sections) + k * width + 1,
                                                  padding + j * (height * 3 + space_between_sections) + l * height + 1,
                                                  width, height))
            unlocked_sections = game_board.get_unlocked_sections()
            s = pygame.Surface((150, 150), pygame.SRCALPHA)  # per-pixel alpha
            if game_board.game_over:
                if winner == 1:
                    s.fill((0, 255, 0, 220))  # notice the alpha value in the color
                else:
                    s.fill((0, 0, 255, 220))  # notice the alpha value in the color
            elif game_board.get_section_owners(game_board.state)[j][i] == 1:
                s.fill((0, 255, 0, 220))  # notice the alpha value in the color
            elif game_board.get_section_owners(game_board.state)[j][i] == 2:
                s.fill((0, 0, 255, 220))  # notice the alpha value in the color
            elif unlocked_sections[j][i] == 1:
                s.fill((255, 255, 255, 128))  # notice the alpha value in the color
            win.blit(s, (padding + i * (width * 3 + space_between_sections), padding + j * (height * 3 +
                                                                                            space_between_sections)))
    if game_board.check_game_over(game_board.state)[0]:
        # print('winner is: Player ', check_game_over(state)[1])
        game_board.game_over, winner = True, game_board.check_game_over(game_board.state)[1]

    # s = pygame.Surface((500, 500), pygame.SRCALPHA)  # per-pixel alpha
    # s.fill((255, 255, 255, 128))  # notice the alpha value in the color
    # win.blit(s, (0, 0))
    pygame.display.update()