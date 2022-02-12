from states.State import State
from pygame import mixer

class PlayingState(State):
    def __init__(self, musicPlayer):
        self.__musicPlayer = musicPlayer

    def play(self):
        pass

    def pause(self):
        mixer.music.pause()
        self.__musicPlayer.getTimeCounter().pauseCounter()
        self.__musicPlayer.setState(self.__musicPlayer.getPausedState())

    def stop(self):
        mixer.music.stop()
        self.__musicPlayer.getTimeCounter().resetCounter()
        self.__musicPlayer.getTimeCounter().notifyObservers()
        self.__musicPlayer.setState(self.__musicPlayer.getStoppedState())

    def seek(self, pos):
        mixer.music.set_pos(pos)
        self.__musicPlayer.getTimeCounter().alterCounter(pos)
