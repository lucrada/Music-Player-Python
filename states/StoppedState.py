from states.State import State
from pygame import mixer

class StoppedState(State):
    def __init__(self, musicPlayer):
        self.__musicPlayer = musicPlayer

    def play(self):
        mixer.music.play(int(not self.__musicPlayer.isRepeating())-1)
        self.__musicPlayer.getTimeCounter().startCounter()
        self.__musicPlayer.setState(self.__musicPlayer.getPlayingState())

    def pause(self):
        pass

    def stop(self):
        pass

    def seek(self, pos):
        mixer.music.play(int(not self.__musicPlayer.isRepeating())-1)
        mixer.music.set_pos(pos)
        mixer.music.pause()
        self.__musicPlayer.getTimeCounter().resetCounter()
        self.__musicPlayer.getTimeCounter().alterCounter(pos)
        self.__musicPlayer.setState(self.__musicPlayer.getPausedState())