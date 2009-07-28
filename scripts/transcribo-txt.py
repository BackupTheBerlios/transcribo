


from optparse import OptionParser
import sys, codecs
from transcribo.plaintext import Writer


parser = OptionParser()

parser.add_option("-t", "--translator", default = 'default',
                  help = """name of the translator (defaults to none;
                  'translator' must be defined in transcribo.renderer.styles.translators).""",
                    metavar="NAME")

parser.add_option("-w", "--wrapper", default = 'indent2',
                  help = """name of the text wrapper (defaults to 'indent2';
                  'wrapper' must be defined in transcribo.renderer.styles.translators).""",
metavar="NAME")

parser.add_option("-f", "--frame", default = 'body1',
                  help = """name of the frame style (defaults to 'body1';
                  'frame' must be defined in transcribo.renderer.styles.translators).""",
metavar="NAME")

parser.add_option("-e", "--encoding", dest = 'enc', default = 'latin1',
                  help="encoding of input and output file, defaults to 'latin1'.",
                    metavar="ENCODING")


parser.add_option("-o", "--output-file", dest = 'explicit_output_file',
                  help = "specify output file, if no input file is given so that a positional argument would be misinterpreted as  input file.",
                  metavar="FILE")

(options, args) = parser.parse_args()

#read source text from file
if args:
    with codecs.open(args.pop(0), 'r', options.enc) as i:
        src = i.read()
else: src = sys.stdin.read()


# render the text
w = Writer(translator_sty = options.translator, wrapper_sty = options.wrapper,
    frame_sty = options.frame)
result = w.render(src)

# save result to file
if options.explicit_output_file: args = [options.explicit_output_file]
if args:
    with codecs.open(args[0], 'w', options.enc) as o:
        o.write(result)
else:
    sys.stdout.write(result)

