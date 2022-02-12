from states.State import State

class EmptyState(State):
    def __init__(self, musicPlayer):
        self.__musicPlayer = musicPlayer

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def seek(self, pos):
        pass