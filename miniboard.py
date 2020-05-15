
class Miniboard:

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
        self.state = [[0 for i in range(3)] for j in range(3)]
        self.owner = 0
        self.last_marked_cell = [-1, -1]

    def print_state(self, state):
        for i in range(3):
            print(state[i])
            print(' ')

    def mark(self, state, player_id, row, col):
        if self.check_valid_mark(state, row, col):
            state[row][col] = player_id
            self.last_marked_cell[0] = row
            self.last_marked_cell[1] = col
            self.check_owned(self.state)
            return True
        return False

    def check_valid_mark(self, state, row, col):
        if self.check_out_of_bounds(row, col):
            print('out of bounds')
            return False
        elif state[row][col] != 0:
            print('already marked cell')
            return False
        elif self.owner != 0:
            print('section owned')
            return False
        return True

    def check_out_of_bounds(self, i, j):
        if 0 <= i <= 2 and 0 <= j <= 2:
            return False
        return True

    def check_unlocked(self):
        return self.owner == 0

    def check_owned(self, state):
        for winning_state in self.WINNING_STATES:
            if self.check_grid_matches_winning_state(state, winning_state, 1):
                self.owner = 1
                return True
            if self.check_grid_matches_winning_state(state, winning_state, 2):
                self.owner = 2
                return True
        return False

    def check_grid_matches_winning_state(self, grid, winning_state, player_id):
        for i in range(3):
            for j in range(3):
                if winning_state[i][j] == 1 and grid[i][j] != player_id:
                    return False
        return True