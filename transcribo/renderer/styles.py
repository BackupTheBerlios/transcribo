import yaml
from transcribo import renderer


def resolve(category, style):
    '''expand inherited styles'''
    if style and style.has_key('parent'): # To do: raise error in case of circularities
       result = resolve(category, category[style['parent']]).copy()
       style.pop('parent')
       result.update(style)
       return result
    else: return style


# load style files and generate dictionary of styles
style_files = [renderer.__path__[0] + '/styles/default.style'] # improve this to load multiple style files from config etc.
stream = ''.join(open(f).read() for f in style_files)
data= yaml.load_all(stream)
styles_dict = {}
for i in data: styles_dict.update(i)
del stream

# resolve inherited styles
for category in styles_dict.values():
    for k, v in category.items():
        category[k] = resolve(category, v)

    

# write style categories into the module to ease access
# Can we write the following functionally thus avoiding all those lines?
content = styles_dict['content']
wrappers = styles_dict['wrappers']
translators = styles_dict['translators']
frames = styles_dict['frames']
hyphenators = styles_dict['hyphenators']
pages = styles_dict['pages']
footers = styles_dict['footers']

del styles_dict