class MusicList:
    def __init__(self):
        self.__list = []
        self.__index = 0

    def addMusic(self, music):
        alreadyExist = False
        for item in self.__list:
            if item.getFileName() == music.getFileName():
                alreadyExist = True
        if not alreadyExist:
            self.__list.append(music)

        self.__list.sort(key=lambda music: music.getFileName())

    def getMusic(self):
        return self.__list[self.__index]

    def getMusicAt(self, index):
        return self.__list[index]

    def getMusicList(self):
        return self.__list

    def setIndex(self, index):
        self.__index = index

    def getIndex(self):
        return self.__index

    def removeMusic(self, index):
        del self.__list[index]

    def incrementIndex(self):
        musicCount = len(self.__list)
        if musicCount == 0:
            return
        if self.__index < musicCount - 1:
            self.__index += 1
            return
        self.__index = 0

    def decrementIndex(self):
        musicCount = len(self.__list)
        if musicCount == 0:
            return
        if self.__index > 0:
            self.__index -= 1
            return
        self.__index = musicCount - 1

    def isEmpty(self):
        return len(self.__list) == 0