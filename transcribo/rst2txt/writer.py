# rst2txt - Docutils writer component for text rendering using Transcribo
# This software is licenced under the GPL.
# Contact the author at fhaxbox66@googlemail.com


try:
    import json
except: ImportError:
    import simplejson as json
    
import docutils.writers
from docutils import frontend
from docutils.nodes import Node, NodeVisitor
from transcribo.renderer import RootFrame, Frame
from transcribo.renderer.content import ContentManager, BaseContent


class Writer(docutils.writers.Writer):

    supported = ('txt', 'brl',)
    
    config_section = 'Braille-specific Options'

    config_section_dependencies = ('writers',)
    
    settings_specs = (
        ('Braille-specific Options', 'no description on this item',
            (
                (
                    "launch editor before writing translated file. Default is 'no'",
                    ('--launch_editor', '-LE'),
                    {'default': 'no',
                        'action': 'store_false',
                        'validator': frontend.validate_boolean
                    }
                ),
                (
                    "specify editor'",
                    ('--editor', '-ED'),
                    {'default': 'nano',
                        'action': 'store_true',
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

    def depart_generic(self, node):
        self.peer.render()
        self.peer = self.peer.parent

    def visit_document(self, node):
        self.root = RootFrame()
    
    
    def depart_document(self, node):
            self.output = self.root.render()
            

    def visit_paragraph(self, node):
        pass

        
    depart_paragraph = depart_generic
    
    
    def visit_Text(self, node):
        self.peer = transcribo.Text(parent = self.peer,
            text = node.astext())

        
    depart_Text = depart_generic
        

