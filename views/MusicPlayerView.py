from tkinter import filedialog
from tkinter import *
from views.View import View
import settings
from utils.convertSecToMin import convertSecToMin

class MusicPlayerView(View):
    def __init__(self, model, controller):
        self.__model = model
        self.__controller = controller

        self.__model.registerObserver(self)
        self.__model.registerTimeCounter(self)
        
        self.__root = Tk()
        self.__root.title('Music Player')
        self.__root.iconphoto(False, PhotoImage(file='assets/icons/icon.png'))
        self.__root.resizable(False, False)

        self.__totalDuration = 0
        self.__totalDurationText = StringVar()
        self.__duration = 0
        self.__durationText = StringVar(value='00:00')
        self.__songName = StringVar()
        self.__repeatText = StringVar(value='OFF')
        self.__volume = DoubleVar(value=settings.INITIAL_VOLUME * 100)
        self.__seekValue = DoubleVar(value=0)

        self.__backgroundColor = '#eee'
        self.__textColor1 = '#000'
        self.__textColor2 = '#fff'
        self.__columnSpacing = 2
        self.__troughColor = '#404040'
        self.__borderColor = '#1c1c1c'
        self.__changeButtonColor = '#696969'
        self.__playButtonColor = '#058503'
        self.__pauseButtonColor = '#032785'
        self.__stopButtonColor = '#85032c'
        self.__repeatButtonColor = '#ab8c00'

        self.__durationTextOptions = {}
        self.__totalDurationTextOptions = {}
        self.__songNameTextOptions = {}
        self.__volumeScaleOptions = {
            'label': 'Volume:',
            'showvalue': 0,
            'sliderlength': 8,
            'width': 8,
            'bd': 0,
            'bg': self.__backgroundColor,
            'fg': self.__textColor1,
            'troughcolor': self.__troughColor,
        }
        self.__seekScaleOptions = {
            'showvalue': 0,
            'sliderlength': 8,
            'length': 300,
            'width': 10,
            'bd': 0,
            'bg': self.__backgroundColor,
            'fg': self.__textColor1,
            'highlightbackground': self.__borderColor,
            'troughcolor': self.__troughColor,
        }
        self.__playButtonOptions = {
            'padx': 12,
            'pady': 7,
            'bg': self.__playButtonColor,
            'fg': self.__textColor2,
            'bd': 0,
            'relief': FLAT,
        }
        self.__pauseButtonOptions = {
            'padx': 12,
            'pady': 7,
            'bg': self.__pauseButtonColor,
            'fg': self.__textColor2,
            'bd': 0,
            'relief': FLAT,
        }
        self.__stopButtonOptions = {
            'padx': 12,
            'pady': 7,
            'bg': self.__stopButtonColor,
            'fg': self.__textColor2,
            'bd': 0,
            'relief': FLAT,
        }
        self.__changeButtonOptions = {
            'padx': 10,
            'pady': 5,
            'bd': 0,
            'bg': self.__changeButtonColor,
            'fg': self.__textColor2,
            'relief': FLAT,
        }
        self.__repeatButtonOptions = {
            'padx': 5,
            'pady': 5,
            'bd': 0,
            'bg': self.__repeatButtonColor,
            'fg': self.__textColor2,
            'relief': FLAT,
        }
        self.__addButtonOptions = {
            'padx': 10,
            'pady': 5,
            'bd': 0,
            'bg': self.__playButtonColor,
            'fg': self.__textColor2,
            'relief': FLAT,
        }
        self.__removeButtonOptions = {
            'padx': 10,
            'pady': 5,
            'bd': 0,
            'bg': self.__stopButtonColor,
            'fg': self.__textColor2,
            'relief': FLAT,
        }
        self.__listBoxOptions = {
            'width': 60,
            'bg': self.__textColor2,
            'bd': 0
        }

        self.__container = Frame(self.__root, bg=self.__backgroundColor)
        self.__musicList = Listbox(self.__container, **self.__listBoxOptions)

        self.__root.configure(bg=self.__backgroundColor)

    def createView(self):
        
        durationText = Label(self.__root, 
        textvariable=self.__durationText, 
        **self.__durationTextOptions
        )

        totalDurationText = Label(self.__root, 
        textvariable=self.__totalDurationText, 
        **self.__totalDurationTextOptions
        )

        songNameText = Label(self.__root, 
        textvariable=self.__songName, 
        **self.__songNameTextOptions
        )

        volumeScale = Scale(self.__root, 
        variable=self.__volume, 
        from_=0, 
        to=100, 
        orient=HORIZONTAL, 
        command=lambda x: self.__controller.setVolume(float(self.__volume.get())),
        **self.__volumeScaleOptions
        )

        seekBarScale = Scale(self.__root, 
        variable=self.__seekValue, 
        from_=0, to=100, 
        orient=HORIZONTAL, 
        command=lambda x: self.__controller.seek(float(self.__seekValue.get()), float(self.__totalDuration)),
        **self.__seekScaleOptions
        )

        buttonColumn = Frame(self.__container)

        addButton = Button(buttonColumn, 
        text="Add", 
        command=lambda: self.__controller.add(filedialog), 
        **self.__addButtonOptions
        )
        
        removeButton = Button(buttonColumn, 
        text="Remove", 
        command=lambda: self.__controller.remove(self.__musicList.curselection()),
        **self.__removeButtonOptions
        )

        prevButton = Button(self.__root, 
        text='Prev', 
        command=self.__controller.prev,
        **self.__changeButtonOptions
        )

        nextButton = Button(self.__root, 
        text='Next', 
        command=self.__controller.next,
        **self.__changeButtonOptions
        )

        playButton = Button(self.__root, 
        text='Play', 
        command=self.__controller.play,
        **self.__playButtonOptions
        )

        pauseButton = Button(self.__root, 
        text='Pause', 
        command=self.__controller.pause,
        **self.__pauseButtonOptions
        )

        stopButton = Button(self.__root, 
        text='Stop', 
        command=self.__controller.stop,
        **self.__stopButtonOptions
        )


        repeatButton = Button(self.__root, 
        textvariable=str(self.__repeatText), 
        command=self.__controller.toggleRepeat,
        **self.__repeatButtonOptions
        )

        songNameText.grid(row=0, columnspan=7, pady=20)
        self.__container.grid(row=1, column=0, columnspan=7, padx=10, pady=10, sticky=W+E)
        self.__musicList.grid(row=0, column=0, columnspan=6, sticky=W+N)
        buttonColumn.grid(row=0, column=6, columnspan=1, sticky=E+N, padx=5)
        addButton.grid(row=0, column=0, sticky=W)
        removeButton.grid(row=1, column=0, sticky=W, pady=5)
        seekBarScale.grid(row=2, column=0, columnspan=7, sticky=W+E, padx=10)
        durationText.grid(row=3, column=0, columnspan=1, sticky=W, padx=15)
        totalDurationText.grid(row=3, column=6, columnspan=1, sticky=E, padx=15)
        volumeScale.grid(row=4, column=0, padx=self.__columnSpacing, pady=20)
        prevButton.grid(row=4, column=1, padx=self.__columnSpacing, pady=20)
        playButton.grid(row=4, column=2, padx=self.__columnSpacing, pady=20)
        pauseButton.grid(row=4, column=3, padx=self.__columnSpacing, pady=20)
        stopButton.grid(row=4, column=4, padx=self.__columnSpacing, pady=20)
        nextButton.grid(row=4, column=5, padx=self.__columnSpacing, pady=20)
        repeatButton.grid(row=4, column=6, padx=self.__columnSpacing, pady=20)
        
        self.__root.mainloop()
        self.__controller.terminateApp()

    def update(self, totalDuration, songName, repeatText, musicList, index):
        if self.__totalDurationText is not None:
            self.__totalDuration = totalDuration
            self.__totalDurationText.set(str(convertSecToMin(int(totalDuration))))
        if self.__songName is not None:
            self.__songName.set('Song Name: ' + songName)
        if self.__repeatText is not None:
            self.__repeatText.set('Repeat: ' + repeatText)

        if len(musicList) == 0:
            self.__musicList.delete(0, END)

        if len(musicList) > 0:
            self.__musicList.delete(0, END)
            for (i,item) in enumerate(musicList):
                self.__musicList.insert(i, f'{item.getFileName()} ({convertSecToMin(int(item.getDuration()))})')
                self.__musicList.activate(index)
                self.__musicList.select_set(index)

    def updateDuration(self, duration):
        self.__duration = duration
        self.__durationText.set(str(convertSecToMin(int(duration))))
        self.__updateSeekValue()

    def __updateSeekValue(self):
        if self.__seekValue is not None and not int(self.__totalDuration) == 0:
            self.__seekValue.set(int(int(self.__duration)*100/int(self.__totalDuration)))
