from yaconfig import Config
import os.path




class Transcriber:

    def __init__(self):
        self.load_config()


    def load_config(self):
        fn = 'config.yaml'
        if os.path.exists(fn): path = '.'
        else: path = __path__[0]
        self.preferences = (yaconfig.Config('/'.join((path, 'config.yaml'))))
