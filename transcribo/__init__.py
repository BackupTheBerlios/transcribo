import logging, os.path
import sys, codecs

# Set up logging to the console and the log file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename ='transcribo.log')

standard_handler = logging.StreamHandler()
formatter = logging.Formatter('%(message)s')
standard_handler.setFormatter(formatter)
logging.getLogger('').addHandler(standard_handler)
logger =logging.getLogger('transcribo')

__all__ = ['renderer', 'yaconfig', 'rST', 'plaintext']





class Transcriber:

    def __init__(self, reader_name='rst', cmd_line = True, styles = []):
        # import Config once as class variable. This would not work outside the class.
        if not hasattr(Transcriber, 'Config'):
          m = __import__('transcribo.yaconfig',globals(), locals(),
          ['transcribo'], -1)
          Transcriber.Config = getattr(m, 'Config')
        self.reader_name = reader_name
        if cmd_line:
            self.parse_cmd_line()
        self.make_styles(stylenames = styles)

    def parse_cmd_line(self):
        from argparse import ArgumentParser
        parser = ArgumentParser(
            description = 'Transcribo - convert rST or plain text into formatted and optionally translated plain text',
            prog = 'transcribe.py',
            fromfile_prefix_chars = '@')
        parser.add_argument('infile', default = 'sys.stdin',
                help = 'file to transcribe, defaults to stdin')
        parser.add_argument('outfile', default = 'sys.stdout',
            help = 'output file for the transcribed document; defaults to stdout')
        parser.add_argument('--reader', choices = ('rst', 'txt'),
            default = 'rst',
            help = 'the desired input format. Choices are rst or txt; defaults to rst')
        parser.add_argument('--styles', nargs = '+', default = [],
            help = 'style files to configure the reader and renderer',
            metavar = 'file_name')

        self.args = parser.parse_args()
        self.reader_name = self.args.reader


    def make_styles(self, stylenames = ['base.yaml']):
        if hasattr(self, 'args'): stylenames = self.args.styles
        for i in range(len(stylenames)):
            if not stylenames[i].endswith('.yaml'):
                stylenames[i] += '.yaml'
        if not 'base.yaml' in stylenames:
            stylenames.insert(0, 'base.yaml')
        if os.path.exists('./transcribo.yaml'):
                stylenames.insert(1, 'transcribo.yaml')
                

        self.cfg = Transcriber.Config()
        for s in stylenames:
            self.cfg.add(s, path = ['./', __path__[0] + '/styles/'])
        self.cfg.inherit()


    def transcribe_file(self, infile = None, outfile = None):
        if not infile: infile = self.args.infile
        with codecs.open(infile, 'r', 'utf8') as i:
            src = i.read()

        if self.reader_name == 'rst':
            from transcribo.rst import transcribe
        elif self.reader_name == 'txt':
            from transcribo.plaintext import transcribe
        output = transcribe(src, self.cfg)
        
        if not outfile: outfile = self.args.outfile
        with codecs.open(outfile, 'w', 'utf8') as o:
            o.write(output)




