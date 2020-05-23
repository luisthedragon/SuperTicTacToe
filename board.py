from miniboard import Miniboard


class Board:
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

    def __init__(self):
        self.state = [[Miniboard() for i in range(3)] for j in range(3)]
        self.last_marked_section = [-1, -1]
        self.game_over = False

    # Only for debug purpose
    def print_state(self, state):
        for i in range(3):
            for j in range(3):
                print(state[i][0].state[j], state[i][1].state[j], state[i][2].state[j])
            print(' ')

    def mark(self, state, player_id, section_row, section_col, element_row, element_col):
        if self.check_valid_mark(state, section_row, section_col, element_row, element_col):
            state[section_row][section_col].mark(state[section_row][section_col].state, player_id, element_row,
                                                 element_col)
            self.last_marked_section[0] = section_row
            self.last_marked_section[1] = section_col
            self.state[section_row][section_col].last_marked_cell[0] = element_row
            self.state[section_row][section_col].last_marked_cell[1] = element_col
            self.check_section_owned(state, section_row, section_col)
            return True
        return False

    def check_valid_mark(self, state, section_row, section_col, element_row, element_col):
        if self.check_out_of_bounds(section_row, section_col, element_row, element_col):
            print('out of bounds')
            return False
        elif state[section_row][section_col].state[element_row][element_col] != 0:
            print('already marked cell')
            return False
        elif state[section_row][section_col].owner != 0:
            print('section owned')
            return False
        elif not self.check_unlocked_section(section_row, section_col):
            print('section locked')
            return False
        return True

    def check_out_of_bounds(self, i, j, k, l):
        if 0 <= i <= 2 and 0 <= j <= 2 and 0 <= k <= 2 and 0 <= l <= 2:
            return False
        return True

    def check_unlocked_section(self, section_row, section_col):
        if self.last_marked_section[0] == -1:
            # print('First turn')
            return True
        if self.get_section_to_unlock(self.state).owner != 0:
            # print('Section to unlock is owned: all sections unlocked')
            return True
        if [section_row, section_col] == self.get_last_marked_cell_of_last_marked_section(self.state):
            # print('Last marked cell unlock this section')
            return True
        return False

    def get_section_to_unlock(self, state):
        return state[self.get_last_marked_cell_of_last_marked_section(state)[0]][
            self.get_last_marked_cell_of_last_marked_section(state)[1]]

    def get_last_marked_cell_of_last_marked_section(self, state):
        return state[self.last_marked_section[0]][self.last_marked_section[1]].last_marked_cell

    def check_section_owned(self, state, section_row, section_col):
        if state[section_row][section_col].owner != 0:
            return True
        return False

    def check_game_over(self, state):
        for winning_state in self.WINNING_STATES:
            if self.check_grid_matches_winning_state(self.get_section_owners(state), winning_state, 1):
                return True, 1
            if self.check_grid_matches_winning_state(self.get_section_owners(state), winning_state, 2):
                return True, 2
        return False, 0

    def get_section_owners(self, state):
        return [[state[i][j].owner for j in range(3)] for i in range(3)]

    def check_grid_matches_winning_state(self, grid, winning_state, player_id):
        for i in range(3):
            for j in range(3):
                if winning_state[i][j] == 1 and grid[i][j] != player_id:
                    return False
        return True

    def get_unlocked_sections(self):
        unlocked_sections = [[0 for i in range(3)] for j in range(3)]
        for i in range(3):
            for j in range(3):
                if self.check_unlocked_section(i, j):
                    unlocked_sections[i][j] = 1
        return unlocked_sections
