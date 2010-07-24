"""
- Transcribo - Reader for reStructuredText. Requires Docutils.
It is also a Docutils writer component.
"""
# This software is licenced under the GPL.
# Contact the author at fhaxbox66@googlemail.com


import docutils
from docutils import writers, nodes
from docutils.core import publish_string
from docutils.nodes import Node, NodeVisitor
from transcribo import logger
from renderer.frames import RootFrame, getFrame
from renderer import pages, utils
from renderer.content import getContentManager, GenericText
from renderer.references import Reference, Target, RefManager



def transcribe(src, styles):

    return publish_string(src, settings_overrides={'output_encoding': 'unicode',
    'input_encoding': 'unicode',
        'styles' : styles},
        writer = Writer())


class Writer(writers.Writer):

    supported = ('txt',)
    
    config_section = 'docutils_txt_writer'

    config_section_dependencies = ('writers',)
    
    settings_specs = ()



    def translate(self):
        self.visitor = TxtVisitor(self.document)
        document = self.document.walkabout(self.visitor)
        self.output = self.visitor.output




class TxtVisitor(NodeVisitor):

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = document.settings
        self.styles = self.settings.styles
        self.ref_man = RefManager()

    def make_refs(self, node):
        r = t = None
        if 'ids' in node and node['ids']:
            t = Target(node['ids'])
            self.ref_man.add_target(t)
        if 'refid' in node:
            r = Reference(node['refid'])
            self.ref_man.add_ref(r)
        return r, t

        
    def visit_block_quote(self, node):
        # create a container frame for the indentations
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'block_quote_container')
        self.parent = self.currentFrame = newFrame


    def depart_block_quote(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent
    

    def visit_bullet_list(self, node):
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'list_container')
        if self.parent is not self.currentFrame:
            newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame
        
        
    def depart_bullet_list(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent
        
        
    def visit_document(self, node):
        current_page_spec = self.styles['page']['default']
        self.paginator = pages.Paginator(self.styles, page_spec = current_page_spec,
        header_spec = None, footer_spec = self.styles['footer']['default'],
        translator_cfg = self.styles['translator']['default'])
        self.root = RootFrame(self.paginator.width)
        self.parent = self.currentFrame = self.root
        self.section_level = 0

    
    
    def depart_document(self, node):
        self.root.render()
        self.output = self.paginator.render(self.root.cache)
            

    def visit_emphasis(self, node): pass
    
    
    def depart_emphasis(self, node): pass
    
    
    visit_enumerated_list= visit_bullet_list
    depart_enumerated_list= depart_bullet_list

            
    
    def visit_list_item(self, node):
        item_style = 'list_item'
        if isinstance(node.parent, nodes.bullet_list):
            # is this a TOC?
            if 'contents' in self.get_classes(node):
                item_style = 'toc_item'
                # autonumbered?
                if 'auto-toc' in node.parent['classes']:
                    itemtext = node[0][0][0][0].astext()
                else: # empty place holder frame
                    itemtext = u' '
            else:
                itemtext = node.parent['bullet']
            
        else: # enumerated list
            itemtext = node.parent['prefix']
            func = utils.__dict__['to_' + node.parent['enumtype']]
            number = node.parent.index(node) + 1
            if 'start' in node.parent:
                number += node.parent['start'] - 1
            itemtext += func(number)
            itemtext += node.parent['suffix']
            
        # frame for the TOC or simplly list item (the section number if present,
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = item_style)
        self.currentFrame = newFrame
        if node is node.parent[0]:
            newFrame.update(y_hook = 'top')

        content = getContentManager(self.styles, newFrame, )
        content.wrapper_cfg = None # this is ugly, I know
        GenericText(content, text = itemtext, translator = self.styles['translator']['default'])
        
        # create a container for the list item body:
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'list_body')
        newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame


    def depart_list_item(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent


    def visit_paragraph(self, node):
        r, t = self.make_refs(node)
        newFrame = getFrame(self.styles, self.currentFrame, self.parent)
        if node is node.parent[0]:
            newFrame.update(y_hook = 'top', y_offset = -1)
        self.currentFrame = newFrame
        self.currentContent = getContentManager(self.styles, self.currentFrame)
            
            
    def depart_paragraph(self, node): pass
        
        
    def visit_section(self, node):
        self.section_level += 1
        # create container frame to allow clean insertion
        # of blank lines before the next section.
        newFrame = getFrame(self.styles, self.currentFrame, self.parent,
            style = 'section_container' + str(self.section_level))
        if self.parent is not self.currentFrame:
            newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame
        r, t = self.make_refs(node)

        
        
        
    def depart_section(self, node):
        self.section_level -= 1
        self.currentFrame = self.parent
        self.parent = self.parent.parent

        
    def visit_strong(self, node): pass
    
    
    def depart_strong(self, node): pass
        
    def visit_literal(self, node): pass # support in  to be implemented
    def depart_literal(self, node): pass


        
    def visit_reference(self, node):
        r, t = self.make_refs(node)
    
    def depart_reference(self, node): pass
        
        
    def visit_target(self, node): pass
    
    
    def depart_target(self, node): pass
    
    
    def visit_Text(self, node):
        font_style = None
        if (isinstance(node.parent, nodes.emphasis) or
            isinstance(node.parent, nodes.strong)):
            font_style = self.styles['translator']['emphasis']
        else:
            c = self.get_classes(node.parent)
            for attr in c:
                if attr in self.styles['translator']:
                    font_style = self.styles['translator'][attr]
                    break
        GenericText(self.currentContent, text = node.astext(), translator = font_style)

        
    def depart_Text(self, node): pass


    def visit_title(self, node):
        r, t = self.make_refs(node)
        if isinstance(node.parent, nodes.section):
            frame_style = 'section_title' + str(self.section_level)
        elif             isinstance(node.parent, nodes.document):
            frame_style = 'document_title'
        elif isinstance(node.parent, nodes.topic):
            frame_style = 'topic'

        newFrame = getFrame(self.styles,
            self.currentFrame, self.parent, style = frame_style)
        self.currentFrame = newFrame
        self.currentContent = getContentManager(self.styles, self.currentFrame,
        style = 'x_align ' + frame_style)
        

    def depart_title(self, node): pass

    def visit_generated(self, node): pass
    def depart_generated(self, node): pass


    def visit_subtitle(self, node):
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'heading0')
        if self.currentFrame == self.parent: # probably supervluous as subtitle can only occur after doctitle
            newFrame.update(y_hook = 'top')
        else:
            newFrame.update(y_hook = 'bottom')
        self.currentFrame = newFrame
        self.currentContent = getContentManager(self.styles, self.currentFrame)

            
    def depart_subtitle(self, node): pass


    def visit_decoration(self, node): pass
    def depart_decoration(self, node): pass
    
    
    def visit_line_block(self, node):
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'list_container') # need custom style for this?
        if self.parent is not self.currentFrame:
            newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame


    def depart_line_block(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent

    def visit_line(self, node):
        newFrame = getFrame(self.styles, self.currentFrame, self.parent)
        self.currentFrame = newFrame
        self.currentContent = getContentManager(self.styles, self.currentFrame, style = 'wrapper pending2')

    def depart_line(self, node): pass
    
    
    
    def visit_topic(self, node): pass
    def depart_topic(self, node): pass
    
    def visit_system_message(self, node):
        logger.log((node['level'] + 1) * 10, 'transcribo.rST.py: DOCUTILS HAS REPORTED AN %s in %s, line %i. Msg Text: %s',
            node['type'], node['source'], node['line'], node[0][0].astext())

    def depart_system_message(self, node): pass
    
    
    def visit_literal_block(self, node): pass # to be revisited
    def depart_literal_block(self, node): pass
    
    
    
    def visit_problematic(self, node): # to be revisited
        logger.error('transcribo.rST.py: Docutils has encountered an unspecified problem.')
            
    def depart_problematic(self, node): pass
    
    
    def visit_transition(self, node):
        # prepare string
        s = self.styles['transition']['default']['text']
        if len(s) == 1:
            s *= int(self.parent.width * self.styles['transition']['default']['ratio'])
            
            # frame for the hor line
        newFrame = getFrame(self.styles, self.currentFrame, self.parent)
        self.currentFrame = newFrame
        self.currentContent = getContentManager(self.styles, self.currentFrame)
        GenericText(self.currentContent, text = s,
            translator = self.styles['transition']['default']['translator'])
        
    
    def depart_transition(self, node): pass
    
    
    def visit_comment(self, node): pass

    def depart_comment(self, node): pass



    def visit_definition_list(self, node):
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'list_container')
        if self.parent is not self.currentFrame:
            newFrame.update(x_anchor = self.currentFrame)
        self.currentFrame = self.parent = newFrame


    def depart_definition_list(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent


    def visit_definition_list_item(self, node):
        # First create a container frame for the whole item. Its first child
        # carries the term and the classifiers, the second child frame carry the definition.
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'standard')
        self.parent = self.currentFrame = newFrame
        # Create frame for term and classifiers
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'glossary_term')
        self.currentFrame = newFrame
        content = getContentManager(self.styles, newFrame)
        # assemble the string of item and classifiers, first the term:
        term_str = node[0][0].astext() + ': '
        # now any classifiers:
        if len(node) > 2:
            term_str += '('
            term_str += '; '.join(n[0].astext() for n in node[1:-1])
            term_str += ')'
        GenericText(content, text = term_str, translator = self.styles['translator']['default']) 


    def depart_definition_list_item(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent


    def visit_term(self, node): pass
    def depart_term(self, node): pass
    def visit_classifier(self, node): pass
    def depart_classifier(self, node): pass
        
        
    def visit_definition(self, node):
        newFrame = getFrame(self.styles, self.currentFrame, self.parent, style = 'glossary_definition')
        self.currentFrame = self.parent = newFrame

        
    def depart_definition(self, node):
        self.currentFrame = self.parent
        self.parent = self.parent.parent


    def get_classes(self, node):
        if node is None: return []
        else:
            c = node['classes'] or []
            c.extend(self.get_classes(node.parent))
            return c
            
            