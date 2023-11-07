import random
import threading
import requests
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "http://web_app:5000/data"

def send_data(device_id):
    while True:
        try:
            value = random.randint(18, 25)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "value": value,
                "timestamp": timestamp,
                "device_id": device_id
            }

            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                logging.info(f"Data sent for {device_id}: {data}")
            else:
                logging.error(f"Failed to send data for {device_id}: {response.text}")

            time.sleep(random.randint(1, 5))

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            time.sleep(10)

def main():
    device_ids = [f"thermometer-{i}" for i in range(1, 7)]

    threads = []
    for device_id in device_ids:
        thread = threading.Thread(target=send_data, args=(device_id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
