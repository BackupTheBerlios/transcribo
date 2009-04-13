from transcribo import logger
from lines import Line
from singleton import get_singleton


class ContentManager:

    def __init__(self, elements,
        wrapper = {'module_name': 'textwrap', 'class_name': 'TextWrapper'},
        translator = None):

        self.elements = elements
        self.wrapper_cfg = wrapper
        self.translator_cfg = translator
        
        

    def render(self, width):
        # Instantiate the wrapper. This is obligatory.
        self.wrapper_cfg['width'] = width
        self.wrapper = get_singleton(**self.wrapper_cfg)
        # instantiate the optional translator. Note that each element may have
        # its own translator. However, the content manager's translator
        # works on the entire content rather than on each element.
        
        if self.translator_cfg:
            self.translator = get_singleton(**self.translator_cfg)
        else:
            self.translator = None
        concat_elements = ''.join([e.render()  for e in self.elements])
        if self.translator: concat_elements = self.translator.translate(concat_elements)
        wrapped = self.wrapper.wrap(concat_elements)
        result = [Line(w) for w in wrapped]
        return result


class BaseContent:

    def __init__(self, content, translator_cfg = None, **args):
        self.content = content
        self.translator_cfg = translator_cfg
        for k,v in args:
            setattr(self, k, v)
        if self.translator_cfg:
            self.translator = get_singleton(**self.translator_cfg)
        else:
            self.translator = None
        
    def render(self):
        if self.translator:
            return self.translator.translate(self.content)
        else:
            return self.content

        