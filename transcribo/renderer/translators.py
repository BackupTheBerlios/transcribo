# Transcribo

"""Translator classes used by Transcribo's renderer. Currently, translation functionality
is implemented in the content.ContentManager and content.GenericText classes.
"""

class UpperTrans:
    '''Translator that merely returns the input string as upper case string. Might be useful to render emphasized text.'''

    def __init__(self):
        pass
        
    def run(self, s):
        return s.upper()
        



class YABTrans:
    '''British Braille translation. Requires the YABT package (http://yabt.berlios.de/).'''
    
    def __init__(self, state = 2):
        '''state = 1: grade 1 Braille; state=2: grade 2 Braille, state=5: computer Braille.'''
        
        from YABT import loaders
        from YABT import translators as yabt_translators
        import pkg_resources
        fileLoader = loaders.BasicXMLFileLoader()
        fileLoader.setInput(pkg_resources.resource_stream("YABT", "tables/britishtobrl.xml"))
        self.bufferedTranslator = yabt_translators.BufferedTranslator()
        self.bufferedTranslator.load(fileLoader)
        self.state = state
        
        
    def run(self, s):
        return self.bufferedTranslator.translate(s, self.state, ' ', ' ')


class Louis:
    '''wrapper for liblouis - a multilingual Braille translation library based
    on brltty. See http://liblouis.googlecode.com). Requires the liblouis shared library or dll (on Windows) as well as the
    Python bindings.'''
    
    def __init__(self, tables = None, mode = 0):
        import louis
        self.louis = louis
        tables[0] = louis.__path__[0] + '/tables/' + tables[0]
        self.tables = tables
        self.mode = mode


    def run(self, s):
        return self.louis.translateString(self.tables, s, self.mode)
        
class NullTrans:
    '''A translator that leaves the text unchanged.'''

    def __init__(self): pass
    
    def run(self, s):
        return s
    