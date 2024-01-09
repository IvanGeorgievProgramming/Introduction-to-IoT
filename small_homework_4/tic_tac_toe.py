import paho.mqtt.client as mqtt
import json

def print_board(board):
    print("   " + "   ".join([str(i) for i in range(len(board))]))
    print(" +---" * len(board) + "+")

    for i, row in enumerate(board):
        row_display = ["-" if cell == "" else cell for cell in row]
        print(str(i) + " | " + " | ".join(row_display) + " |")
        print(" +---" * len(board) + "+")

def is_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True

    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True

    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False

def is_board_full(board):
    return all(all(row) for row in board)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("tic_tac_toe/player_move")

def on_message(client, userdata, msg):
    if msg.topic == "tic_tac_toe/player_move":
        move = json.loads(msg.payload)
        process_player_move(move)

def process_player_move(move):
    global board, current_player
    row, col = move['row'], move['col']
    if valid_move(row, col):
        board[row][col] = current_player
        print_board(board)
        if is_winner(board, current_player):
            client.publish("tic_tac_toe/game_state", json.dumps({"state": "win", "board": board, "player": current_player}))
            reset_game()
        elif is_board_full(board):
            client.publish("tic_tac_toe/game_state", json.dumps({"state": "draw", "board": board}))
            reset_game()
        else:
            switch_player()
    else:
        print("Invalid move")

def valid_move(row, col):
    return 0 <= row <= 2 and 0 <= col <= 2 and not board[row][col]

def switch_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"
    client.publish("tic_tac_toe/game_state", json.dumps({"state": "turn", "player": current_player}))

def reset_game():
    global board, current_player
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-dashboard.com", 1883, 60)
client.loop_start()

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
client.publish("tic_tac_toe/game_state", json.dumps({"state": "turn", "player": current_player}))

while True:
    pass
