
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description

from transcribo import rst2txt

publish_cmdline(writer = rst2txt.Writer(), description = default_description)

