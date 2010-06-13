from yaconfig import Config
import os.path, sys
from argparse import ArgParser



class Transcriber:

    def __init__(self, src_name = '', dest_name = '',
        src = None, dest = None, front_end = None, styles = []):
        if src: self.src = src
        elif src_name: self.src = codec.open(src_name, 'utf8')
        else: self.src = sys.stdin
        
if dest: self.dest = dest
elif dest_name: self.dest = codec.open(dest_name, 'w', 'utf8')
else: self.dest = sys.stdout
        self.dest = dest
        
        if front_end: self.front_end = front_end
        else:
            self.front_end = __import__(front_end_name)
# configure front end
        self.styles = styles
        


    def load_config(self):
        fn = 'config.yaml'
        if os.path.exists(fn): path = '.'
        else: path = __path__[0]
        self.preferences = (yaconfig.Config('/'.join((path, 'config.yaml'))))
