from pygame import mixer
from utils.exceptions.FileNotSupportedException import FileNotSupportedException
import settings
import uuid

class Music:
    def __init__(self, filename):
        mixer.init()
        self.__checkFileCompatibility(filename)
        self.__id = str(uuid.uuid4())
        self.__filename = filename
        self.__duration = str(int(mixer.Sound.get_length(mixer.Sound(settings.MUSIC_FILES_LOCATION + self.__filename))))

    def getFileName(self):
        return self.__filename

    def getDuration(self):
        return self.__duration

    def getId(self):
        return self.__id

    def __checkFileCompatibility(self, filename):
        fileIsSupported = False
        for filetype in settings.SUPPORTED_FILE_FORMATS:
            if filename.endswith(filetype):
                fileIsSupported = True
        if not fileIsSupported:
            raise FileNotSupportedException('The given file type is not supported!')