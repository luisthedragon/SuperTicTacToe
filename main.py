"""
*** *** ***
*** *** ***
*** *** ***

*** *** ***
*** *** ***
*** *** ***

*** *** ***
*** *** ***
*** *** ***
"""

import pygame

section_owners = [[0 for i in range(3)] for j in range(3)]
last_marked_cell = [-1, -1, -1, -1]
WINNING_STATES = [[[1, 1, 1],
                   [0, 0, 0],
                   [0, 0, 0]],
                  [[0, 0, 0],
                   [1, 1, 1],
                   [0, 0, 0]],
                  [[0, 0, 0],
                   [0, 0, 0],
                   [1, 1, 1]],
                  [[1, 0, 0],
                   [1, 0, 0],
                   [1, 0, 0]],
                  [[0, 1, 0],
                   [0, 1, 0],
                   [0, 1, 0]],
                  [[0, 0, 1],
                   [0, 0, 1],
                   [0, 0, 1]],
                  [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]],
                  [[0, 0, 1],
                   [0, 1, 0],
                   [1, 0, 0]]]


def print_state(state):
    for i in range(3):
        for j in range(3):
            print(state[i][0][j], state[i][1][j], state[i][2][j])
        print(' ')


def mark(state, player_id, section_row, section_col, element_row, element_col):
    if check_valid_mark(state, section_row, section_col, element_row, element_col):
        state[section_row][section_col][element_row][element_col] = player_id
        last_marked_cell[0] = section_row
        last_marked_cell[1] = section_col
        last_marked_cell[2] = element_row
        last_marked_cell[3] = element_col
        check_section_owned(state, section_row, section_col)
        return True

    return False


def check_valid_mark(state, section_row, section_col, element_row, element_col):
    if state[section_row][section_col][element_row][element_col] != 0:
        print('already marked cell')
        return False
    elif section_owners[section_row][section_col] != 0:
        print('section owned')
        return False
    elif not check_unlocked_section(section_row, section_col):
        print('section locked')
        return False
    return True


def check_unlocked_section(section_row, section_col):
    if last_marked_cell[0] == -1:
        # print('First turn')
        return True
    if section_owners[last_marked_cell[2]][last_marked_cell[3]] != 0:
        # print('Section to unlock is owned: all sections unlocked')
        return True
    if section_row == last_marked_cell[2] and section_col == last_marked_cell[3]:
        # print('Last marked cell unlock this section')
        return True
    return False


def check_section_owned(state, section_row, section_col):
    for winning_state in WINNING_STATES:
        if check_grid_matches_winning_state(state[section_row][section_col], winning_state, 1):
            section_owners[section_row][section_col] = 1
            return True
        if check_grid_matches_winning_state(state[section_row][section_col], winning_state, 2):
            section_owners[section_row][section_col] = 2
            return True
    return False


def check_game_over(state):
    for winning_state in WINNING_STATES:
        if check_grid_matches_winning_state(section_owners, winning_state, 1):
            return True, 1
        if check_grid_matches_winning_state(section_owners, winning_state, 2):
            return True, 2
    return False, 0


def check_grid_matches_winning_state(grid, winning_state, player_id):
    for i in range(3):
        for j in range(3):
            if winning_state[i][j] == 1 and grid[i][j] != player_id:
                return False
    return True


def get_unlocked_sections():
    unlocked_sections = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            if check_unlocked_section(i, j):
                unlocked_sections[i][j] = 1
    return unlocked_sections


def main():
    state = [[[[0 for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
    state[0][0][0][0] = state[0][0][1][1] = state[0][0][2][2] = state[1][1][1][2] = 1
    # print_state(state)
    # print(check_section_owned(state, 0, 0))
    # print(mark(state, 1, 0, 0, 0, 0))
    # print(mark(state, 2, 0, 0, 1, 1))
    # print(mark(state, 2, 1, 2, 0, 0))
    # print(mark(state, 2, 2, 2, 0, 0))
    # print(mark(state, 1, 0, 0, 2, 2))
    # print(mark(state, 2, 1, 1, 1, 2))
    # print(mark(state, 1, 2, 2, 0, 2))
    # print(mark(state, 2, 2, 2, 1, 2))
    # print(mark(state, 1, 1, 1, 1, 2))
    # print(mark(state, 1, 1, 2, 1, 2))
    # print_state(state)
    # Testing check_game_over function
    # section_owners[0][0] = section_owners[0][1] = section_owners[0][2] = 2

    # main loop
    # player_id = 1
    # while True:
    #     mark_request = list(map(int, input().split()))
    #     while not mark(state, player_id, mark_request[0], mark_request[1], mark_request[2], mark_request[3]):
    #         mark_request = list(map(int, input().split()))
    #     player_id = player_id % 2 + 1
    #     print_state(state)
    #     print(section_owners)


# main()

state = [[[[0 for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
# state[0][0][0][0] = state[0][0][1][1] = state[0][0][2][2] = state[1][1][1][2] = 1

pygame.init()

win_width = win_height = 462
space_between_sections = 3
width, height = 50, 50
padding = (win_width - width * 9 - space_between_sections * 2) // 2

win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("SUPER TIC TAC TOE")

current_player_id = 1
game_over = False
run = True
while run:

    pygame.time.delay(300)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                i, j, k, l = event.pos[1] // 150, event.pos[0] // 150, event.pos[1] // 50 % 3, event.pos[0] // 50 % 3
                # state[i][j][k][l] = (state[i][j][k][l] + 1) % 3
                if mark(state, current_player_id, i, j, k, l):
                    current_player_id = current_player_id % 2 + 1

    # pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    # for i in range(9):
    #     for j in range(9):
    #         pygame.draw.rect(win, (255, 0, 0), (i * width, j * height, width, height))
    #         pygame.draw.rect(win, (0, 0, 0), (i * width + 1, j * height + 1, width - 2, height - 2))
    # i: section_col j: section_row k: cell_col l: cell_row
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if state[j][i][l][k] == 0:
                        color = (255, 0, 0)
                    elif state[j][i][l][k] == 1:
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    pygame.draw.rect(win, (0, 0, 0), (padding + i * (width * 3 + space_between_sections) + k * width,
                                                      padding + j * (height * 3 + space_between_sections) + l * height,
                                                      width, height))
                    pygame.draw.rect(win, color, (padding + i * (width * 3 + space_between_sections) + k * width + 1,
                                                  padding + j * (height * 3 + space_between_sections) + l * height + 1,
                                                  width, height))
            unlocked_sections = get_unlocked_sections()
            s = pygame.Surface((150, 150), pygame.SRCALPHA)  # per-pixel alpha
            if game_over:
                if winner == 1:
                    s.fill((0, 255, 0, 220))  # notice the alpha value in the color
                else:
                    s.fill((0, 0, 255, 220))  # notice the alpha value in the color
            elif section_owners[j][i] == 1:
                s.fill((0, 255, 0, 220))  # notice the alpha value in the color
            elif section_owners[j][i] == 2:
                s.fill((0, 0, 255, 220))  # notice the alpha value in the color
            elif unlocked_sections[j][i] == 1:
                s.fill((255, 255, 255, 128))  # notice the alpha value in the color
            win.blit(s, (padding + i * (width * 3 + space_between_sections), padding + j * (height * 3 +
                                                                                            space_between_sections)))
    if check_game_over(state)[0]:
        # print('winner is: Player ', check_game_over(state)[1])
        game_over, winner = True, check_game_over(state)[1]

    # s = pygame.Surface((500, 500), pygame.SRCALPHA)  # per-pixel alpha
    # s.fill((255, 255, 255, 128))  # notice the alpha value in the color
    # win.blit(s, (0, 0))
    pygame.display.update()
