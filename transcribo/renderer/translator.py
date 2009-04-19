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

        
        
    
    