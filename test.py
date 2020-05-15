from miniboard import Miniboard

boardcito = Miniboard()
player_id = 1
while boardcito.check_unlocked():
    r, c = list(map(int, input().strip().split()))
    boardcito.mark(boardcito.state, player_id, r, c)
    boardcito.print_state(boardcito.state)
    player_id = (player_id % 2) + 1
