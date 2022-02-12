from views.MusicPlayerView import MusicPlayerView
import settings

class MusicPlayerController:
    def __init__(self, model):
        self.__model = model
        self.__view = MusicPlayerView(model, self)
        self.__model.notifyObservers()
        self.__model.setVolume(settings.INITIAL_VOLUME)
        self.__view.createView()

    def play(self):
        self.__model.play()

    def pause(self):
        self.__model.pause()

    def stop(self):
        self.__model.stop()

    def setVolume(self, volume):
        self.__model.setVolume(volume/100)

    def seek(self, pos, maxDuration):
        self.__model.seek((pos * maxDuration)/100)

    def next(self):
        self.__model.next()
    
    def prev(self):
        self.__model.prev()

    def remove(self, index):
        if not len(index) == 0:
            self.__model.removeMusic(index[0])

    def add(self, filedialog):
        filenames = filedialog.askopenfilenames(title='Select music files', initialdir='/', filetypes=(('mp3 file', '*.mp3'), ('wav file', '*.wav')))
        self.__model.addMusic(filenames)

    def toggleRepeat(self):
        self.__model.toggleRepeat()

    def terminateApp(self):
        self.__model.terminateThreads()
