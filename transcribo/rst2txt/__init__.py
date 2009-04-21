# rst2txt - Docutils writer component for text rendering using Transcribo
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

    def get_frame(self, style, parent):
        frame_cfg = styles.frame[style] # ToDo: allow deviations from hard-coded styles
        translator_cfg = styles.translator['default'] # ToDo: create translator according to settings, eg. Braille
        if style.endswith('0'):
            wrapper_cfg = styles.wrappers['simple'] # ToDo: as before
        else:
            wrapper_cfg = styles.wrappers['indent2']
        return Frame(parent = parent, content = ContentManager(wrapper = wrapper_cfg,
            translator = translator_cfg),
            **frame_cfg)
        

    def visit_document(self, node):
        self.root = RootFrame() # ToDo: make it customizable, eg. by passing page settings
        self.current = self.root
        self.parent = self.root

    
    
    def depart_document(self, node):
            self.output = self.root.render()
            

    def visit_paragraph(self, node):
        # determine context and set style accordingly
        index = node.parent.index(node)
        if isinstance(node.parent, nodes.document) or isinstance(node.parent, nodes.section):
            element_style = 'normal'
        else:
            element_style = 'default'
        if index == 0: element_style += '0'
        self.previous = self.current
        self.current = self.get_frame(element_style, self.parent)
        self.current.x_anchor = self.current.parent
        if index == 0:
            self.current.y_anchor = self.current.parent
            self.current.y_hook = 'top'
        else:
            self.current.y_anchor = self.previous
            self.current.y_hook = 'bottom'
            
            
    def depart_paragraph(self, node): pass
        
    
    def visit_Text(self, node):
         self.current.content.elements.append(GenericText(content = node.astext()))

        
    def depart_Text(self, node): pass

        

