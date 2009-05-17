"""Singleton pattern"""

register = []


def get_singleton(**args):
    '''return an instance of the class specified by class_path(**args)
    
    Only keyword arguments are allowed. class_path must be passed as
    keyword . It is popped from args before instantiating class_name. If a keyword argument's value v is
    itself a dictionary containing a key 'class_path', get_singleton is called recursively
    with **v as argument.'''
    
    
    for r in register:
        if args == r[0]: return r[1]
    else:
        args2 = args.copy()
        class_path = args2.pop('class_path')
        module_name, class_name = class_path.rsplit('.', 1)
        for k, v in args2.items():
            if isinstance(v, dict) and 'class_path' in v:
                args2[k] = get_singleton(**v)
        m = __import__(module_name, globals(), locals(), [class_name], -1)
        c = getattr(m, class_name)
        result = c(**args2)
        register.append((args, result))
        return result
        