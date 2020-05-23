from board import Board
from network import Network
import pygame

pygame.init()

# DRAW VARIABLES
win_width = win_height = 500  # before: 462
space_between_sections = 10  # before: 3
width, height = 50, 50
padding = (win_width - width * 9 - space_between_sections * 2) // 2

win = pygame.display.set_mode((win_width, win_height))
game_board = Board()

pygame.display.set_caption("SUPER TIC TAC TOE")


player = 1

run = True

def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(f"{game.wins[p]} : {game.wins[(p + 1) % 2]}", 1, (100, 255, 255))
        win.blit(text, (260, 50))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(f"Player {p + 1}", 1, (20, 20, 20))
        win.blit(text, (240, 100))

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        # for btn in btns:
        #     btn.draw(win)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    win.fill((20, 20, 20))

    while run:

        pygame.time.delay(300)
        try:
            game_board = n.send('get')
        except:
            run = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    i, j, k, l = (event.pos[1] - padding) // (space_between_sections + height * 3), \
                                 (event.pos[0] - padding) // (space_between_sections + width * 3), \
                                 (event.pos[1] - padding) % (space_between_sections + 3 * height) // height, \
                                 (event.pos[0] - padding) % (space_between_sections + 3 * width) // width
                    print(i, j, k, l)

                    # game_board.mark(game_board.state, player, i, j, k, l)
                    if not game_board.check_out_of_bounds(i, j, k, l):
                        n.send(f"mark {i} {j} {k} {l}")

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
                        pygame.draw.rect(win, (0, 0, 0),
                                         (padding + i * (width * 3 + space_between_sections) + k * width,
                                          padding + j * (height * 3 + space_between_sections) + l * height,
                                          width, height))
                        pygame.draw.rect(win, color,
                                         (padding + i * (width * 3 + space_between_sections) + k * width + 1,
                                          padding + j * (height * 3 + space_between_sections) + l * height + 1,
                                          width, height))
                unlocked_sections = game_board.get_unlocked_sections()
                s = pygame.Surface((150, 150), pygame.SRCALPHA)  # per-pixel alpha
                if game_board.game_over:
                    if game_board.winner == 1:
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

        # s = pygame.Surface((500, 500), pygame.SRCALPHA)  # per-pixel alpha
        # s.fill((255, 255, 255, 128))  # notice the alpha value in the color
        # win.blit(s, (0, 0))
        pygame.display.update()

        # redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
