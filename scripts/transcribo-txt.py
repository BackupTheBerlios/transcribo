


from optparse import OptionParser
import sys, codecs
from transcribo.plaintext import Writer


parser = OptionParser()
parser.add_option("-t", "--translator", type = 'string', dest = 'translator', default = 'default',
                  help="""name of the translator (defaults to none;
                  'translator' must be defined in transcribo.renderer.styles.translators).""",
                    metavar="TRANSLATOR_NAME")
parser.add_option("-o", "--output-file", dest = 'output_file',
                  help="""explicitly specify the output file.
                  This is only needed when not specifying an input file to use stdin.""")

(options, args) = parser.parse_args()



# allow usage in pipes. 'args' stores the input and output file or file-name afterwards.
if not args: args = [sys.stdin] # if no input file is specified
if options.output_file:
    if len(args) == 2: raise ValueError('Two output file names given, one allowed.')
    else: args.append(options.output_file)
elif len(args) == 1: args.append(sys.stdout)

(input_file, output_file) = args

if isinstance(input_file, str): # otherwise it is stdin, so nothing to open
    src_file = codecs.open(input_file, 'r', 'utf8')
else: src_file = sys.stdin

src = src_file.read()
if src_file is not sys.stdin: src_file.close()

translator = options.translator
    
w = Writer(translator_sty = translator)
result = w.render(src)

if isinstance(output_file, str):
    with codecs.open(output_file, 'w', 'utf8') as o:
        o.write(result)
else: output_file.write(result) # to stdout

