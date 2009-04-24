"""
rst2txt - Docutils writer component for text rendering using Transcribo
"""
# This software is licenced under the GPL.
# Contact the author at fhaxbox66@googlemail.com


    
import docutils.writers
from docutils import frontend, nodes
from docutils.nodes import Node, NodeVisitor
from transcribo.renderer import RootFrame, Frame
from transcribo.renderer.content import ContentManager, GenericText
import styles




class Writer(docutils.writers.Writer):

    supported = ('brl',)
    
    config_section = 'rst2txt'

    config_section_dependencies = ('writers',)
    
    settings_specs = (
        ('rst2txt', 'no description on this item',
            (
                (
                    "Braille translation, default is 'no'",
                    ('--braille', '-brl'),
                    {'default': 0,
                        'action': 'store_true',
                        'validator': frontend.validate_boolean
                    }
                ),
                (
                    "Pagination, default is 'no''",
                    ('--pagination', '-PG'),
                    {'default': 'no',
                        'action': 'store_false',
                        'validator': frontend.validate_boolean
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

    def getContentManager(self, style):
        content_cfg = styles.content[style]
        translator_cfg = styles.translator[style]
        wrapper_cfg = styles.wrappers['indent2']
        return ContentManager(wrapper = wrapper_cfg,
            translator = translator_cfg,
            **content_cfg)


    def getFrame(self, style):
        frame_cfg = styles.frame[style] # ToDo: allow deviations from hard-coded styles
        return Frame(parent = self.parent,
        x_anchor = self.parent, y_anchor = self.currentFrame,
                    **frame_cfg)
        

    def visit_document(self, node):
        self.root = RootFrame() # ToDo: make it customizable, eg. by passing page settings
        self.parent = self.root
        self.currentFrame = self.root
        self.section_level = 0

    
    
    def depart_document(self, node):
            self.output = self.root.render()
            

    def visit_paragraph(self, node):
        # determine context and set style accordingly
        index = node.parent.index(node)
        frame_style = 'body1'
        newFrame = self.getFrame(frame_style)
        self.currentContent = self.getContentManager('body1')
        newFrame += self.currentContent
        if index == 0:
            newFrame.update(y_hook = 'top')
        else:
            newFrame.update(y_hook = 'bottom')
        self.currentFrame = newFrame
            
            
    def depart_paragraph(self, node): pass
        
        
    def visit_section(self, node):
        self.section_level += 1
        
        
        
    def depart_section(self, node):
        self.section_level -= 1
        
        
        
    def visit_Text(self, node):
         self.currentContent += GenericText(text = node.astext())

        
    def depart_Text(self, node): pass

    def visit_title(self, node):
        if isinstance(node.parent, nodes.section):
            frame_style = 'heading' + str(self.section_level)
            newFrame = self.getFrame(frame_style)
            # first frame within this parent frame?
            if self.currentFrame == self.parent:
                newFrame.update(y_hook = 'top')
            else:
                newFrame.update(y_hook = 'bottom')
            self.currentContent = self.getContentManager(frame_style)
            newFrame += self.currentContent
            self.currentFrame = newFrame
        else:
            raise TypeError('Cannot handle title node in this context (parent = %s' % node.parent)


    def depart_title(self, node): pass
