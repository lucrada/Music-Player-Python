from states.State import State
from pygame import mixer

class PausedState(State):
    def __init__(self, musicPlayer):
        self.__musicPlayer = musicPlayer

    def play(self):
        mixer.music.unpause()
        self.__musicPlayer.getTimeCounter().startCounter()
        self.__musicPlayer.setState(self.__musicPlayer.getPlayingState())

    def pause(self):
        pass

    def stop(self):
        mixer.music.stop()
        self.__musicPlayer.getTimeCounter().resetCounter()
        self.__musicPlayer.getTimeCounter().notifyObservers()
        self.__musicPlayer.setState(self.__musicPlayer.getStoppedState())

    def seek(self, pos):
        mixer.music.set_pos(pos)
        self.__musicPlayer.getTimeCounter().alterCounter(pos)
        mixer.music.pause()
