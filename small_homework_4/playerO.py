import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("tic_tac_toe/game_state")

def on_message(client, userdata, msg):
    if msg.topic == "tic_tac_toe/game_state":
        game_state = json.loads(msg.payload)
        handle_game_state(game_state)

def handle_game_state(game_state):
    if game_state["state"] == "turn" and game_state["player"] == MY_PLAYER_ID:
        make_move()
    elif game_state["state"] in ["win", "draw"]:
        print(f"Game Over: {game_state['state']}")

def make_move():
    row = int(input("Enter row: "))
    col = int(input("Enter column: "))
    client.publish("tic_tac_toe/player_move", json.dumps({"row": row, "col": col}))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-dashboard.com", 1883, 60)
client.loop_start()

MY_PLAYER_ID = "O"

while True:
    pass
