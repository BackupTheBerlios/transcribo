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

    def getFrame(self, style):
        frame_cfg = styles.frame[style] # ToDo: allow deviations from hard-coded styles
        translator_cfg = styles.translator['default'] # ToDo: create translator according to settings, eg. Braille
        if style.endswith('0'):
            wrapper_cfg = styles.wrappers['simple'] # ToDo: as before
        else:
            wrapper_cfg = styles.wrappers['indent2']
        return Frame(parent = self.parent,
        x_anchor = self.parent, y_anchor = self.previous,
        content = ContentManager(wrapper = wrapper_cfg,
            translator = translator_cfg),
            **frame_cfg)
        

    def visit_document(self, node):
        self.root = RootFrame() # ToDo: make it customizable, eg. by passing page settings
        self.parent = self.root
        self.previous = self.root
        self.section_level = 0

    
    
    def depart_document(self, node):
            self.output = self.root.render()
            

    def visit_paragraph(self, node):
        # determine context and set style accordingly
        index = node.parent.index(node)
        element_style = 'body1'
        current = self.getFrame(element_style)
        if index == 0:
            current.update(y_hook = 'top')
            current.content.wrapper_cfg['initial_indent'] = '  '
        else:
            current.update(y_hook = 'bottom')
        self.previous = current
            
            
    def depart_paragraph(self, node): pass
        
    def visit_section(self, node):
        self.section_level += 1
        
        
        
    def depart_section(self, node):
        self.section_level -= 1
        
        
        
    def visit_Text(self, node):
         self.previous.content += GenericText(content = node.astext())

        
    def depart_Text(self, node): pass

    def visit_title(self, node):
        if isinstance(node.parent, nodes.section):
            frame_style = 'heading' + str(self.section_level)
            try:
                current = self.getFrame(frame_style)
            except KeyError:
                    current = self.getFrame('default_heading')
            # first frame within this parent frame?
            if self.previous == self.parent:
                current.update(y_hook = 'top')
            else:
                current.update(y_hook = 'bottom')
            self.previous = current

    def depart_title(self, node): pass
