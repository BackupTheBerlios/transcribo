import yaml, re, codecs, os.path



# regex for string interpolation. '$' must enclose the path to the source string.
interpolate_re = re.compile(r'\$[^$]+\$')

class Config(dict):
    '''
    Load mappings from multiple YAML files and merge them
    recursively. This is especially useful to implement cascading style sheets and
    other complex cpnfig tasks. Supports multiple inheritance between
    npdes, arbitrary nesting levels for the dictionaries and string interpolation.
    '''
    
    
        

    def __getattr__(self, name):
        return self[name]
        
    def __setattr__(self, name, value):
        self[name] = value
        
    def __delattr__(self, name):
        self.remove(name)
        
    def add(self, infile, path = []):
        '''Load YAML file and merge the resulting data recursively into the tree of dictionaries.

'infile': a file name (string or unicode) or file-like object 
path: a list of path names to search each file name; defaults to [].
        '''
        
        if isinstance(infile, basestring): # it must be a file name
            stream = None
            for p in path:
                s = '/'.join((p, infile))
                if os.path.exists(s):
                    stream = codecs.open(s, 'r', 'utf8')
                    break
                        
            # If no path was given, stream is still None. So open it
            if not stream: stream = codecs.open(infile, 'r', 'utf8')
                    
        else: # must be a file-like object
            stream = infile
        data= self.dict2Config(yaml.load(stream.read()))
        stream.close()
        self.merge(data)

        
    def dict2Config(self, d):
        if not isinstance(d, dict): raise Typeerror('dict expected.')
        if not isinstance(d, Config): d = Config(d)
        for k in d:
            if isinstance(d[k], dict):
                d[k] = Config(d[k])
                self.dict2Config(d[k])
        return d
        
        
    def merge(self, d):
        '''recursively update the dictionary of config items'''
        
        if not isinstance(d, dict): raise TypeError('dict expected.')
        for k in d:
            if (k in self and isinstance(self[k], Config)
                and isinstance(d[k], Config)):
                self[k].merge(d[k])
            else: self[k] = d[k]
        
        
    def find_node(self, path, scope):
        path_list = path.split('/')
        
        # If the path has no /, it can be a local one pointing to a sibling of node:
        if len(path_list) == 1 and path in scope:
            return (scope[path], scope)
            
        # Traverse the path to get the node instance to inherit from.
        node = self
        while path_list:
            scope = node
            node = node[path_list.pop(0)]
        return (node, scope)

    
    def inherit(self):
        '''resolve inheritances. '''
        
        def walk(node, scope):

            # Inheritance of current node
            if node.has_key('inherits_from'):
                # In case of single inheritance: convert attribute into a list for looping
                if isinstance(node['inherits_from'], basestring):
                    node['inherits_from'] = [node['inherits_from']]

                # process each ancester (in case of single or multiple inheritance)
                for p in node['inherits_from']:
                    (parent_node, scope2) = self.find_node(p, scope)
                    # recursively resolve any inheritance relations of that parent node
                    walk(parent_node, scope2)

                # Actually perform the inheritance of this node
                for i, j in parent_node.items():
                    node.setdefault(i, j)
                    
                # Remove the inheritance indicator from the node. Future
                # traversals will treat the node as not inheriting anything.
                node.pop('inherits_from')
                
            # process all children of the current node:
            for k in node:
                if isinstance(node[k], dict) and node not in visited: walk(node[k], node)

            # mark this node as visited to avoid future visits
            visited.append(node)


        visited = [] # avoid multiple visits
        walk(self, {})
    
    
    def interpolate(self):
        '''String interpolation similar to ConfigParser from the standard library.'''
        
        def walk(node, scope):
        
            if node not in visited:
                # Check for string values to interpolate
                for k in node:
                    if isinstance(node[k], basestring):
                        for var in interpolate_re.findall(node[k]):
                            # get the result string to insert in place of var. Delimitors must be trimmed before.
                            (result, scope) = self.find_node(var[1:-1], scope)
                            node[k] = node[k].replace(var, result, 1)
                    elif isinstance(node[k], dict):
                        walk(node[k], node)
                visited.append(node)


        visited = [] # avoid multiple visits
        walk(self, {})
                    

        
        
    