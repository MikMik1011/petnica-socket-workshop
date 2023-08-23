import threading
from time import sleep

def printInterval(text, interval):
    while True:
        print(text)
        sleep(interval)

thread1 = threading.Thread(target=printInterval, args=("Hello", 1))
thread2 = threading.Thread(target=printInterval, args=("World", 2))

thread1.start()
thread2.start()