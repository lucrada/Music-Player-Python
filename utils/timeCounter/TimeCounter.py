# Time counter keeps track of the duration of the currently playing music
# and update the view accordingly

from threading import Thread
import time

class TimeCounter:
    def __init__(self):
        self.__duration = 0
        self.__thread = None
        self.__start = False

        self.__observers = []
    
    def __runCounter(self):
        while self.__start:
            self.__duration += 1
            self.notifyObservers()
            time.sleep(1)

    def startCounter(self):
        self.__start = True
        if (self.__thread is None) or (not self.__thread.is_alive()):
            self.__thread = Thread(target=self.__runCounter)
            self.__thread.start()

    def alterCounter(self, seconds):
        self.__duration = int(seconds)

    def pauseCounter(self):
        self.__start = False

    def resetCounter(self):
        self.__duration = 0
        self.__start = False

    def getDuration(self):
        return self.__duration

    def registerObserver(self, observer):
        self.__observers.append(observer)

    def notifyObservers(self):
        for observer in self.__observers:
            observer.updateDuration(self.__duration)