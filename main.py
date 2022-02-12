from models.MusicPlayerModel import MusicPlayerModel
from controllers.MusicPlayerController import MusicPlayerController

model = None

try:
    model = MusicPlayerModel()
    controller = MusicPlayerController(model)
except:
    if model is not None:
      model.terminateThreads()