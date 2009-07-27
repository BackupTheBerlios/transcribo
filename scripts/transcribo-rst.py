
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

# make Docutils use custom config file
import sys
if '--config' not in sys.argv:
    sys.argv.insert(1, 'transcribo-rst.conf')
    sys.argv.insert(1, '--config')


from docutils.core import publish_cmdline, default_description

from transcribo import rST

publish_cmdline(writer = rST.Writer(), description = default_description)

