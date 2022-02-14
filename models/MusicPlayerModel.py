from pygame import mixer
import shutil
import settings
import os
from states.PausedState import PausedState
from states.PlayingState import PlayingState
from states.StoppedState import StoppedState
from states.EmptyState import EmptyState
from models.Music import Music
from utils.musicList.MusicList import MusicList
from utils.timeCounter.TimeCounter import TimeCounter
from utils.endEventListener.EndEventListener import EndEventListener

class MusicPlayerModel:
    def __init__(self):
        self.__playingState = PlayingState(self)
        self.__pausedState = PausedState(self)
        self.__stoppedState = StoppedState(self)
        self.__emptyState = EmptyState(self)
        self.__state = self.__stoppedState

        self.__currentMusicId = None

        self.__timeCounter = TimeCounter()
        self.__endEventListener = EndEventListener(self)

        self.__repeat = False

        self.__musicList = MusicList()
        self.__fetchMusicList()
        
        mixer.init()

        self.__endEventListener.runListener()

        if (not self.__musicList.isEmpty()):
            self.load(self.__musicList.getMusic())

        self.setVolume(settings.INITIAL_VOLUME)

        self.__observers = []

    def __fetchMusicList(self):
        files = os.listdir(settings.MUSIC_FILES_LOCATION)
        for file in files:
            for supportedFileFormat in settings.SUPPORTED_FILE_FORMATS:
                if file.endswith(supportedFileFormat):
                    self.__musicList.addMusic(Music(file))
        if self.__musicList.isEmpty():
            self.setState(self.__emptyState)
        if not self.__musicList.isEmpty() and self.__state == self.__emptyState:
            self.setState(self.__stoppedState)
            self.load(self.__musicList.getMusic())

    def load(self, music):
        mixer.music.load(settings.MUSIC_FILES_LOCATION + music.getFileName())
        self.__currentMusicId = music.getId()

    def play(self):
        self.__state.play()

    def pause(self):
        self.__state.pause()

    def stop(self):
        self.__state.stop()

    def seek(self, pos):
        self.__state.seek(pos)

    def next(self):
        if not self.__state == self.__emptyState:
            self.__timeCounter.resetCounter()
            self.__musicList.incrementIndex()
            self.load(self.__musicList.getMusic())
            if self.__state == self.__pausedState:
                self.setState(self.__stoppedState)
            if self.__state == self.__playingState:
                self.stop()
                self.play()
                self.__timeCounter.startCounter()
        
            self.notifyObservers()
        
    def prev(self):
        if not self.__state == self.__emptyState:
            self.__timeCounter.resetCounter()
            self.__musicList.decrementIndex()
            self.load(self.__musicList.getMusic())
            if self.__state == self.__pausedState:
                self.setState(self.__stoppedState)
            if self.__state == self.__playingState:
                self.stop()
                self.play()
                self.__timeCounter.startCounter()
            
            self.notifyObservers()

    def addMusic(self, filenames):
        if filenames:
            for filename in filenames:
                shutil.copy(filename, settings.MUSIC_FILES_LOCATION + os.path.basename(filename))
            self.__fetchMusicList()
            self.notifyObservers()

    def removeMusic(self, index):
        musicToRemove = self.__musicList.getMusicAt(index)
        if musicToRemove.getId() == self.__currentMusicId:
            self.next()
            self.__musicList.setIndex(index)
        if len(self.__musicList.getMusicList()) == 1:
            self.__endEventListener.terminateListener()
            self.__timeCounter.resetCounter()
            mixer.music.unload()
            self.setState(self.__emptyState)
        os.remove(settings.MUSIC_FILES_LOCATION + musicToRemove.getFileName())
        self.__musicList.removeMusic(index)
        self.notifyObservers()

    def toggleRepeat(self):
        if not self.__state == self.__emptyState:
            self.__repeat = not self.__repeat
            self.__handleRepeat()
            self.notifyObservers()

    def __handleRepeat(self):
        currentPos = self.__timeCounter.getDuration()
        mixer.music.play(int(not self.isRepeating())-1, start=currentPos)
        if self.__state == self.__pausedState:
            mixer.music.pause()
            self.__timeCounter.pauseCounter()
        if self.__state == self.__stoppedState:
            mixer.music.stop()
            self.__timeCounter.resetCounter()

    def isRepeating(self):
        return self.__repeat

    def setVolume(self, volume):
        mixer.music.set_volume(volume)

    def setState(self, state):
        self.__state = state

    def getPlayingState(self):
        return self.__playingState
    
    def getPausedState(self):
        return self.__pausedState
    
    def getStoppedState(self):
        return self.__stoppedState

    def getMusicList(self):
        return self.__musicList

    def getTimeCounter(self):
        return self.__timeCounter

    def registerObserver(self, observer):
        self.__observers.append(observer)

    def registerTimeCounter(self, observer):
        self.__timeCounter.registerObserver(observer)

    def notifyObservers(self):
        totalDuration = self.__musicList.getMusic().getDuration() if not self.__musicList.isEmpty() else 0
        filename = self.__musicList.getMusic().getFileName() if not self.__musicList.isEmpty() else 'Empty Playlist'
        repeatText = 'ON' if self.__repeat else 'OFF'
        if self.__observers:
            for observer in self.__observers:
                observer.update(totalDuration, filename, repeatText, self.__musicList.getMusicList(), self.__musicList.getIndex())

    def terminateThreads(self):
        if mixer.get_busy():
            mixer.stop()
            mixer.unload()
        self.__timeCounter.resetCounter()
        self.__endEventListener.terminateListener()