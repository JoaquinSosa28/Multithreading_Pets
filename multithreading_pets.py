import threading
import time
from enum import Enum
import random

thread_lock = threading.Lock()

#Animal's owner enum
class Animal(Enum):
    Alicia = 0
    Bernardo = 1
    Joaquin = 2
    Matias = 3
    Agustin = 4

#Animal behaviour class/thread that handles every dog
class AnimalBehaviour(threading.Thread):
    def __init__(self, threadID, animal, garden_time, waiting_time):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.animal = animal
        self.garden_time = garden_time
        self.waiting_time = waiting_time

    def run(self):
        print(f"Starting thread: id:{self.threadID}, animal:{self.animal.name}")
        while True:
            #Always after the sleep try to access the garden if it hasn't been locked by another thread
            time.sleep(random.randint(waiting_time[0], waiting_time[1]))
            thread_lock.acquire()
            set_animal(self.animal, garden_time)
            thread_lock.release()

#Print which animal is in the garden and sleep for as long as needed
def set_animal(animal, garden_time):
    print(f"{animal.name}'s pet is in the garden")
    time_in_garden = random.uniform(garden_time[0], garden_time[1])
    time.sleep(time_in_garden)
    #print(f"Time: {random.uniform(1, 2.5)}")
    print(f"{animal.name}'s pet is no longer in the garden. ({time_in_garden})")

if __name__ == "__main__":
    #Get the amount of time the animals will spend in the garden and waiting to comeback
    print("Enter the range of seconds for garden and waiting separated with a bar ex: num1-num2")
    garden_time = input("Enter the range of seconds the animals will stay in the garden: ")
    waiting_time = input("Enter the range of seconds the animals will wait to return to the garden: ")
    
    #Spliting and parsing it into ints
    garden_time = garden_time.split('-')
    for i in range(len(garden_time)):
        garden_time[i] = float(garden_time[i])
    
    waiting_time = waiting_time.split('-')
    for i in range(len(waiting_time)):
        waiting_time[i] = int(waiting_time[i])
    
    #Sort it so it doesn't matter in which order you input the number ex: 9-2 == 2-9
    garden_time = sorted(garden_time)
    waiting_time = sorted(waiting_time)
    
    #Create the threads
    threadID = 0
    threads = []
    for animal in Animal:
        threads.append(AnimalBehaviour(threadID, animal, garden_time, waiting_time))
        threadID += 1

    #Start threads start at the same time and which one will enter the garden first is yet declared
    for thread in threads:
        thread.start()

    #print(f"{threading.current_thread()}")
