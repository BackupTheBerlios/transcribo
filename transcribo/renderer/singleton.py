"""Singleton pattern"""

register = []


def get_singleton(**args):
    '''return an instance of module_name.class_name(...)
    
    Only keyword arguments are allowed. module_name and class_name must be passed as
    keyword . These are popped from args before instantiating class_name. If a keyword argument's value v is
    itself a dictionary containing a key 'module_name', get_singleton is called recursively
    with **v as argument.'''
    
    
    for r in register:
        if args == r[0]: return r[1]
    else:
        args2 = args.copy()
        module_name = args2.pop('module_name')
        class_name = args2.pop('class_name')
        for k, v in args2.items():
            if isinstance(v, dict) and 'module_name' in v:
                args2[k] = get_singleton(**v)
    m = __import__(module_name, globals(), locals(), [class_name], -1)
    c = getattr(m, class_name)
    result = c(**args2)
    register.append([args, result])
    return result
        