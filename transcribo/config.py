import yaml
from transcribo import renderer

class Config(dict):
    def __init__(self, files):
        '''
        Load one or more YAML files and store them successively
        in the instance (it is in essence a dictionary).
        When processing each file, the nexted config items are merged. The merge
        rules that apply when an iten duplicate keys occur are as follows:
        
        * override all data except for dictionaries
        * update dictionaries whereby the previous rule applies to items in the dictionary

        Arguments:
        
        'files': a file name or list of file names
        '''
        
        
        
        self.input_files = []
        self.add(files)

    def add(self, files):
        '''Load one or more YAML files and merge the resulting data into any existing dictionaries.'''
        if isinstance(files, basestring): files = [files]
        self.input_files.extend(files)
        for f in files:
            data= yaml.load(open(f).read())
            self.merge(data)
        self.resolve_inheritances(self      )
        
        
        
    def merge(self, *args, **kwargs):
        '''recursively update the dictionary of config items'''
        
        def mix_in(d1, d2):
            for k in d2:
                if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
                    mix_in(d1[k], d2[k])
                else: d1[k] = d2[k]
            
        # Construct from the arguments the dict to be mixed in
        d = {}
        if args: d = args[0]
        if kwargs: d.update(kwargs)
        mix_in(self, d)
        

    
    
    def resolve_inheritances(self, node):
        '''resolve inheritances. '''
        # first, process all children of the current node:
        for k in node:
                if isinstance(node[k], dict): self.resolve_inheritances(node[k])
                
                # Inheritance of current node
        if node.has_key('inherits_from'): 
            # In case of single inheritance: convert attribute into a list for looping
            if isinstance(node['inherits_from'], basestring):
                node['inherits_from'] = [node['inherits_from']]
                
            # process each ancester (in case of single or multiple inheritance)
            for p in node['inherits_from']:
                path = p.split('.')
                # Traverse the path to get the node instance to inherit from.
                parent_node = self
                while path: parent_node = parent_node[path.pop(0)]
                # recursively resolve any inheritance relations of the parent node
                self.resolve_inheritances(parent_node)
            
                # Actually perform the inheritance
                for i, j in parent_node.items():
                    node.setdefault(i, j)
            # Remove the inheritance indicator from the node. Future
            # traversals will treat the node as not inheriting anything.
            node.pop('inherits_from')

