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
        self.state = [[[[0 for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]
        self.section_owners = [[0 for i in range(3)] for j in range(3)]
        self.last_marked_cell = [-1, -1, -1, -1]
        self.game_over = False

    # Only for debug purpose
    def print_state(self, state):
        for i in range(3):
            for j in range(3):
                print(state[i][0][j], state[i][1][j], state[i][2][j])
            print(' ')

    def mark(self, state, player_id, section_row, section_col, element_row, element_col):
        if self.check_valid_mark(state, section_row, section_col, element_row, element_col):
            state[section_row][section_col][element_row][element_col] = player_id
            self.last_marked_cell[0] = section_row
            self.last_marked_cell[1] = section_col
            self.last_marked_cell[2] = element_row
            self.last_marked_cell[3] = element_col
            self.check_section_owned(state, section_row, section_col)
            return True
        return False

    def check_valid_mark(self, state, section_row, section_col, element_row, element_col):
        if self.check_out_of_bounds(section_row, section_col, element_row, element_col):
            print('out of bounds')
            return False
        elif state[section_row][section_col][element_row][element_col] != 0:
            print('already marked cell')
            return False
        elif self.section_owners[section_row][section_col] != 0:
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
        if self.last_marked_cell[0] == -1:
            # print('First turn')
            return True
        if self.section_owners[self.last_marked_cell[2]][self.last_marked_cell[3]] != 0:
            # print('Section to unlock is owned: all sections unlocked')
            return True
        if section_row == self.last_marked_cell[2] and section_col == self.last_marked_cell[3]:
            # print('Last marked cell unlock this section')
            return True
        return False

    def check_section_owned(self, state, section_row, section_col):
        for winning_state in self.WINNING_STATES:
            if self.check_grid_matches_winning_state(state[section_row][section_col], winning_state, 1):
                self.section_owners[section_row][section_col] = 1
                return True
            if self.check_grid_matches_winning_state(state[section_row][section_col], winning_state, 2):
                self.section_owners[section_row][section_col] = 2
                return True
        return False

    def check_game_over(self, state):
        for winning_state in self.WINNING_STATES:
            if self.check_grid_matches_winning_state(self.section_owners, winning_state, 1):
                return True, 1
            if self.check_grid_matches_winning_state(self.section_owners, winning_state, 2):
                return True, 2
        return False, 0

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
