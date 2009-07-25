"""
rst2txt - Docutils writer component for text rendering using Transcribo
"""
# This software is licenced under the GPL.
# Contact the author at fhaxbox66@googlemail.com


    
import docutils.writers
from docutils import frontend, nodes
from docutils.nodes import Node, NodeVisitor
from transcribo.renderer.frames import RootFrame, Frame
from transcribo.renderer import pages, utils, styles
from transcribo.renderer.content import ContentManager, GenericText
from transcribo import logger




class Writer(docutils.writers.Writer):

    supported = ('brl',)
    
    config_section = 'docutils_txt_writer'

    config_section_dependencies = ('writers',)
    
    settings_specs = (
        ('Options specific to  Transcribo`s docutils_txt_writer', 'no description on this item',
            (
                (
                    "Braille translation, default is 'no'",
                    ('--translator', '-tl'),
                    {'default': None,
                        'type': 'str'
                    }
                ),
                (
                    "Page width, default is 60'",
                    ('--page_width'),
                    {'default': 60,
                        'type': 'int'
                    }
                )
            )
        )
    )



    def translate(self):
        self.visitor = TxtVisitor(self.document)
        document = self.document.walkabout(self.visitor)
        self.output = self.visitor.output




class TxtVisitor(NodeVisitor):

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        # Convert some settings to int
        for s in ['page_width']:
            v = getattr(self.settings, s)
            setattr(self.settings, s, int(v))
        
        
        

    def getContentManager(self, content_style = 'default', translator_style = None, wrapper_style = 'default'):
        if not translator_style:
            translator_style = self.settings.translator
        translator_cfg = styles.translators[translator_style]
        try:
            content_cfg = styles.content[content_style]
        except KeyError:
            content_cfg = styles.content['simple']
        try:
            wrapper_cfg = styles.wrappers[wrapper_style]
        except KeyError:
            wrapper_cfg = styles.wrappers['simple']
        return ContentManager(parent = self.currentFrame, wrapper = wrapper_cfg,
            translator = translator_cfg,
            **content_cfg)


    def getFrame(self, style):
        frame_cfg = styles.frame[style]
        result = Frame(parent = self.parent,
        x_anchor = self.parent, y_anchor = self.currentFrame,
        **frame_cfg)
        if self.parent == self.currentFrame:
            result.update(y_hook = 'top')
        else:
            result.update(y_hook = 'bottom')
        return result
        
        
    def visit_block_quote(self, node):
        # create a container frame for the indentations
        newFrame = self.getFrame('block_quote_container')
        self.parent = self.currentFrame = newFrame


    def depart_block_quote(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent

    

    def visit_bullet_list(self, node):
        newFrame = self.getFrame('list_container')
        if self.parent is not self.currentFrame:
            newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame
        
        
    def depart_bullet_list(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent
        
        
        

    def visit_document(self, node):
        self.paginator = pages.Paginator(page_spec = styles.pages['default'],
        header_spec = None, footer_spec = styles.footers['default'],
        translator_cfg = styles.translators[self.settings.translator])
        self.root = RootFrame(max_width = self.paginator.width)
        self.parent = self.currentFrame = self.root
        self.section_level = 0

    
    
    def depart_document(self, node):
        self.root.render()
        self.output = self.paginator.render(self.root.cache)
            

    def visit_emphasis(self, node): pass
    
    
    def depart_emphasis(self, node): pass
    
    
    def visit_enumerated_list(self, node):
        newFrame = self.getFrame('list_container')
        if self.parent is not self.currentFrame:
            newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame


    def depart_enumerated_list(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent

            
    def visit_list_item(self, node):
        # First create a container frame for the whole item. Its first child}
        # carries the bullet point or enumerator, the following child frames carry the actual content.
        newFrame = self.getFrame('list_item_container')
        self.parent = self.currentFrame = newFrame
        newFrame = self.getFrame('list_item')
        if isinstance(node.parent, nodes.bullet_list):
            itemtext = node.parent['bullet']
        else: # enumerated_list
            itemtext = node.parent['prefix']
            func = utils.__dict__['to_' + node.parent['enumtype']]
            number = node.parent.index(node) + 1
            if node.parent.hasattr('start'):
                number += node.parent['start'] - 1
            itemtext += func(number)
            itemtext += node.parent['suffix']
        content = ContentManager(newFrame, wrapper = styles.wrappers['simple'])
        GenericText(content, text = itemtext, translator = styles.translators['default']) # write a getGenericText factory function?
        self.currentFrame = newFrame



    def depart_list_item(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent
            


    def visit_paragraph(self, node):
        newFrame = self.getFrame('body1')
        
        # handle the first paragraph within a list item frame
        if isinstance(node.parent, nodes.list_item):
            newFrame.update(**styles.frame['list_body'])
            newFrame.update(x_anchor = self.parent[0])
            if len(self.parent) == 2:
                newFrame.update(y_hook = 'top')
        self.currentFrame = newFrame
        self.currentContent = self.getContentManager()

            
            
    def depart_paragraph(self, node): pass
        
        
    def visit_section(self, node):
        self.section_level += 1
        
        
        
    def depart_section(self, node):
        self.section_level -= 1
        
        
    def visit_strong(self, node): pass
    
    
    def depart_strong(self, node): pass
        
    def visit_reference(self, node): pass
    
    def depart_reference(self, node): pass
        
        
    def visit_target(self, node): pass
    
    
    def depart_target(self, node): pass
    
    
    def visit_Text(self, node):
        if (isinstance(node.parent, nodes.emphasis) or
            isinstance(node.parent, nodes.strong)):
            font_style = styles.translators['emphasis']
        else: font_style = None
        GenericText(self.currentContent, text = node.astext(), translator = font_style)

        
    def depart_Text(self, node): pass


    def visit_title(self, node):
        if isinstance(node.parent, nodes.section) or isinstance(node.parent, nodes.document):
            frame_style = 'heading' + str(self.section_level)
            newFrame = self.getFrame(frame_style)
            # first frame within this parent frame?
            if self.currentFrame == self.parent:
                newFrame.update(y_hook = 'top')
            else:
                newFrame.update(y_hook = 'bottom')
            self.currentFrame = newFrame
            self.currentContent = self.getContentManager(content_style = 'heading0')
        else:
            raise TypeError('Cannot handle title node in this context (parent = %s' % node.parent)


    def depart_title(self, node): pass



    def visit_subtitle(self, node):
        newFrame = self.getFrame('heading0')
        if self.currentFrame == self.parent: # probably supervluous as subtitle can only occur after doctitle
            newFrame.update(y_hook = 'top')
        else:
            newFrame.update(y_hook = 'bottom')
        self.currentFrame = newFrame
        self.currentContent = self.getContentManager(content_style = 'heading0')

            
    def depart_subtitle(self, node): pass