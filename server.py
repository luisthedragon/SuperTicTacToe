import socket
from _thread import *
import pickle
from board import Board

server = "192.168.56.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def broadcast(conns, data):
    for conn in conns:
        conn.sendall(pickle.dumps(data))


def threaded_client(conns, connId, p, gameId):
    global idCount
    conn = conns[connId]
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            print('recv: data:', data)

            if gameId in games:
                game = games[gameId]
                # game.print_state(game.state)
                if not data:
                    break
                else:
                    if data.startswith('mark'):
                        i, j, k, l = int(data[5]), int(data[7]), int(data[9]), int(data[11])
                        # print(p, i, j, k, l)
                        if game.p1_turn and p == 1 or not game.p1_turn and p == 2:
                            # print(game.p1_turn, p == 1, not game.p1_turn, p == 2)
                            if game.mark(game.state, p, i, j, k, l):
                                game.p1_turn = not game.p1_turn

                                if game.check_game_over(game.state)[0]:
                                    # print('winner is: Player ', check_game_over(state)[1])
                                    game.game_over, game.winner = game.check_game_over(game.state)
                                broadcast(conns, game)
                                # print('broadcast:', pickle.dumps(game))
                    else:
                        conn.sendall(pickle.dumps(game))
                        print('sendall:', pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


conns = []
while True:
    conn, addr = s.accept()
    conns.append(conn)
    print("Connected to:", addr)

    idCount += 1
    p = 1
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Board()
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 2

    start_new_thread(threaded_client, (conns, idCount-1, p, gameId))
