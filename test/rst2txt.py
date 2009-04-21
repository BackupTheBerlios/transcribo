
try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass




from docutils.core import publish_cmdline, default_description

from transcribo import rst2txt

w = rst2txt.Writer()


publish_cmdline(writer = w, description = default_description)

