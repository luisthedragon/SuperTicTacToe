from _thread import start_new_thread
from network import Network
import random
import pygame

pygame.init()
pygame.font.init()

# DRAW VARIABLES
screen_width = screen_height = 600  # before: 462
space_between_sections = 10  # before: 3
width, height = 50, 50
padding = (screen_width - width * 9 - space_between_sections * 2) // 2

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("SUPER TIC TAC TOE")

player = 1

run = True


def random_play(game_board):
    random_mark = list()
    unlocked_sections = game_board.get_unlocked_sections(game_board.state)
    for i, row in enumerate(unlocked_sections):
        for j, cell in enumerate(row):
            if unlocked_sections[i][j]:
                random_mark.append(i)
                random_mark.append(j)
                for _ in range(2):
                    random_mark.append(random.randint(0, 2))
                return random_mark


def redraw_window(screen, game_board, player):
    """

    :type game_board: Board
    """
    screen.fill((40, 100, 20)) if player==1 else screen.fill((40, 20, 100))
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render(f'Player {player}', 1, (100, 255, 255))
    text_rect = text.get_rect(center=(screen_width / 2, 30))
    screen.blit(text, text_rect)

    if not game_board.game_over:
        if (player-1) != game_board.p1_turn:
            text = font.render(f'Your turn', 1, (100, 255, 255))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height - 30))
            screen.blit(text, text_rect)
    else:
        if player == game_board.winner:
            text = font.render(f'You win', 1, (100, 255, 255))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height - 30))
            screen.blit(text, text_rect)
        else:
            text = font.render(f'You lose', 1, (100, 255, 255))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height - 30))
            screen.blit(text, text_rect)

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
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (padding + i * (width * 3 + space_between_sections) + k * width,
                                      padding + j * (height * 3 + space_between_sections) + l * height,
                                      width, height))
                    pygame.draw.rect(screen, color,
                                     (padding + i * (width * 3 + space_between_sections) + k * width + 1,
                                      padding + j * (height * 3 + space_between_sections) + l * height + 1,
                                      width, height))
            unlocked_sections = game_board.get_unlocked_sections(game_board.state)
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
            screen.blit(s, (padding + i * (width * 3 + space_between_sections), padding + j * (height * 3 +
                                                                                            space_between_sections)))
    pygame.display.update()


def recv_game(n, game_boards):
    while True:
        try:
            data = n.recv()
            print('recv: data:', data)
            if not data:
                break
            else:
                print('received!')
                game_boards[0] = data
        except:
            break


def main():
    run = True
    n = Network()
    game_boards = [None]
    n.send('get')
    game_boards[0] = n.recv()
    start_new_thread(recv_game, (n, game_boards))
    player = int(n.getP())
    print("You are player", player)
    screen.fill((20, 20, 20))

    while run:
        game_board = game_boards[0]
        pygame.time.delay(300)

        redraw_window(screen, game_board, player)

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
                    if not game_board.check_out_of_bounds(i, j, k, l) and not game_board.game_over:
                        n.send(f"mark {i} {j} {k} {l}")

        # Random player for test purposes :)
        # if not game_board.game_over:
        #     i,j,k,l = random_play(game_board)
        #     n.send(f"mark {i} {j} {k} {l}")

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text, text_rect)
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
