
import transcribo
from  transcribo import yaconfig
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
    help = 'style files to configure the reader and renderer')


args = parser.parse_args()

# Generate the styles dict
if not 'base.yaml' in args.styles:
    args.styles.insert(0, 'base.yaml')

cfg = yaconfig.Config()
for s in args.styles:
    if not s.endswith('.yaml'): s += '.yaml'
    cfg.add(s, path = ['./', transcribo.__path__[0] + '/styles/'])
    

from transcribo.renderer import factory
factory.styles.update(cfg)

if args.reader == 'rst':
    from docutils.core import publish_file, default_description
    from transcribo import rst
    publish_file(source_path = args.infile,
                destination_path = args.outfile,
            writer = rst.Writer())
            
elif args.reader == 'txt':
    pass
    

