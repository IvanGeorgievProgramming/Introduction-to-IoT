import json
import time
import threading

class Bulb:
    def __init__(self, thing_id, bulb_number):
        self.thing_id = self.policy_id = thing_id
        self.file_name = thing_id + ".json"
        self.event = threading.Event()
        self.attributes = {
            "manufacturer": "OnlyLeds",
            "number": bulb_number,
        }
        self.features = {
            "colorControl": {
                "properties": {
                    "color": "red",
                },
                "desiredProperties": {
                    "color": "white"
                }
            },
            "brightnessControl": {
                "properties": {
                    "brightness": 69,
                },
                "desiredProperties": {
                    "brightness": 255
                }
            },
            "stateControl": {
                "properties": {
                    "state": "on",
                },
                "desiredProperties": {
                    "state": "off"
                }
            },
            "state": {
                "properties": {
                    "working": True
                }
            },
        }

    def save_to_json(self):
        serializable = {
            "thingId": self.thing_id,
            "policyId": self.policy_id,
            "attributes": self.attributes,
            "features": self.features
        }
        with open("./digital-twins/" + self.file_name, 'w') as output:
            json.dump(serializable, output, indent=4, ensure_ascii=False)

    def break_bulb(self):
        print("Bulb number " + str(self.attributes["number"]) + " is broken")
        self.features["state"]["properties"]["working"] = False
        self.save_to_json()

    def fix_bulb(self, tech_id):
        print("Technician " + str(tech_id) + " is fixing bulb number " + str(self.attributes["number"]))
        time.sleep(5)
        print("Bulb number " + str(self.attributes["number"]) + " is fixed")
        self.features["state"]["properties"]["working"] = True
        self.save_to_json()

    def update_color_control(self, color):
        self.features["colorControl"]["properties"]["color"] = color
        self.save_to_json()

    def update_brightness_control(self, brightness):
        self.features["brightnessControl"]["properties"]["brightness"] = brightness
        self.save_to_json()

    def update_state_control(self, state):
        self.features["stateControl"]["properties"]["state"] = state
        self.save_to_json()

    def print_feature(self):
        print("Bulb number " + str(self.attributes["number"]) + " is " + self.features["colorControl"]["properties"]["color"] + " and has brightness " + str(self.features["brightnessControl"]["properties"]["brightness"]) + " and is " + self.features["stateControl"]["properties"]["state"])
