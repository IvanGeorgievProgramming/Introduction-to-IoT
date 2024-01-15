import paho.mqtt.client as mqtt
import sys
import time

broker = "broker.hivemq.com"
port = 1883
topic = "accessControl/1"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client.connect(broker, port, 60)

client.loop_start()

last_send_time = 0
send_interval = 5

while True:
    current_time = time.time()
    if current_time - last_send_time >= send_interval:
        code = input("Enter access code: ")
        if code.lower() == "exit":
            break
        client.publish(topic, code)
        print(f"Sent code '{code}' to topic '{topic}'")
        last_send_time = time.time()
        time.sleep(send_interval)

client.loop_stop()
client.disconnect()