import time
import random
import threading
from queue import Queue

from bulb import Bulb

BULBS = 5
TECHNICIANS = 3

colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "white"]
brightnesses = [i for i in range(101)]

def bulb_functioning(bulb, stop_event):
    while not stop_event.is_set():
        if random.randint(0, 100) < 40:
            bulb.break_bulb()
            manager_queue.put(bulb)
            manager_event.set()
        else:
            color = random.choice(colors)
            brightness = random.choice(brightnesses)
            bulb.update_color_control(color)
            bulb.update_brightness_control(brightness)
            bulb.print_feature()
        time.sleep(random.randint(3, 5))

def technician_fix_bulb(technician_id, bulb, stop_event):
    while not stop_event.is_set():
        bulb.fix_bulb(technician_id)
        available_technicians.put(technician_id)
        return

def manager(stop_event):
    while not stop_event.is_set():
        manager_event.wait()
        while not manager_queue.empty():
            if not available_technicians.empty():
                t = threading.Thread(target=technician_fix_bulb, args=(available_technicians.get(), manager_queue.get(), stop_event))
                t.start()
                t.join()

if __name__ == "__main__":
    stop_event = threading.Event()
    manager_queue = Queue()
    manager_event = threading.Event()
    available_technicians = Queue()

    manager_thread = threading.Thread(target=manager, args=(stop_event,))
    manager_thread.start()

    for i in range(TECHNICIANS):
        available_technicians.put(i + 1)

    bulbs = [Bulb("bulb-" + str(num), num) for num in range(1, BULBS + 1)]
    bulb_threads = [threading.Thread(target=bulb_functioning, args=(bulb, stop_event)) for bulb in bulbs]

    for bt in bulb_threads:
        bt.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        manager_thread.join()
        for bt in bulb_threads:
            bt.join()
        print("Shutting down...")
