import yaml
from transcribo import renderer


style_files = [renderer.__path__[0] + '/styles/default.style'] # improve this to load multiple style files from config etc.

stream = ''.join(open(f).read() for f in style_files)

data= yaml.load_all(stream)
styles_dict = {}
for i in data: styles_dict.update(i)
del stream

# Can we write the following functionally thus avoiding all those lines?
content = styles_dict['content']
wrappers = styles_dict['wrappers']
translators = styles_dict['translators']
frames = styles_dict['frames']
frame = styles_dict['frame']
hyphenators = styles_dict['hyphenators']
pages = styles_dict['pages']
footers = styles_dict['footers']
