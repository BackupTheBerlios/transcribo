"""
plaintext - frontend for the Transcribo text renderer
"""
# This software is licenced under the GPL.
# Contact the author at fhaxbox66@googlemail.com



import transcribo
from transcribo.renderer.frames import RootFrame, Frame
from transcribo.renderer import pages, utils
from transcribo.renderer.content import GenericText, ContentManager
from renderer.factory import getContentManager, getFrame, styles
from transcribo import logger



class Writer:

    def __init__(self, page_sty = 'default', frame_sty = 'default',
        translator_sty = 'default', wrapper_sty = 'indent2', footer_sty = 'default'):
        self.page_sty = page_sty
        self.frame_sty = frame_sty
        self.translator_sty = translator_sty
        self.wrapper_sty = wrapper_sty
        self.footer_sty = footer_sty
        

    def render(self, text):
        self.paginator = pages.Paginator(page_spec = styles['page'][self.page_sty],
        header_spec = None, footer_spec = styles['footer'][self.footer_sty],
        translator_cfg = styles['translator'][self.translator_sty])
        self.root = RootFrame(max_width = self.paginator.width)
        
        # prepare the text
        # appending an empty line simplifies handling of paragraphs at the very end of the text. 
        lines = text.splitlines()
        lines.append(u'')
        

        # assemble paragraphs
        paragraphs = []
        l = len(lines)
        in_paragraph = False
        for i in range(l):
            # beginning of paragraph
            if not (in_paragraph or lines[i].isspace() or lines[i] == u''):
                in_paragraph = True
                start = i
            # end of paragraph
            elif in_paragraph and (lines[i].isspace() or lines[i] == u''):
                paragraphs.append(u' '.join(lines[start:i]))
                in_paragraph = False


        # build the frame. Each paragraph gets one
        cfg = styles['frame'][self.frame_sty].copy()
        for p in paragraphs:
            if len(self.root):
                cfg.update(x_anchor = self.root[-1], y_anchor = self.root[-1], y_hook = 'bottom')
            else:
                cfg.update(x_anchor = self.root, y_anchor = self.root, y_hook = 'top')
            f = Frame(self.root, **cfg)

            cm = ContentManager(f, wrapper = styles['wrapper'][self.wrapper_sty],
                translator = None)
            GenericText(cm, text = p)
        
        # render the frame
        self.root.render()
        return self.paginator.render(self.root.cache)
            
