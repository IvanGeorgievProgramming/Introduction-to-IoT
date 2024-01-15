import paho.mqtt.client as mqtt
import time

broker = "broker.hivemq.com"
port = 1883
topic = "accessControl/1"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    code = msg.payload.decode()
    if code == "123#":
        print("Wiper - 123#: The LED goes off for 5 seconds, the flow through the relay is interrupted.")
        time.sleep(5)
        print("LED goes back on, door locked.")
    elif code == "456#":
        print("Keeper - 456#: The diode goes out for 5 seconds, the flow through the relay is interrupted.")
        time.sleep(5)
        print("Diode back on, door locked.")
    else:
        print("Unknown - Door remains locked.")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

client.loop_forever()
