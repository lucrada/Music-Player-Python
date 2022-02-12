from threading import Thread

class EndEventListener:
    def __init__(self, model):
        self.__model = model
        self.__timeCounter = self.__model.getTimeCounter()
        self.__thread = None
        self.__start = True

    def listen(self):
        while self.__start:
            if not self.__model.getMusicList().isEmpty():
                if int(self.__timeCounter.getDuration()) >= int(self.__model.getMusicList().getMusic().getDuration()):
                    if self.__model.isRepeating():
                        self.__timeCounter.resetCounter()
                        self.__timeCounter.startCounter()
                    else:
                        self.__timeCounter.resetCounter()
                        self.__model.next()

    def runListener(self):
        self.__thread = Thread(target=self.listen)
        self.__thread.start()

    def terminateListener(self):
        self.__start = False
