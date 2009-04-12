register = []


def get_singleton(**args):
    module_name = args.pop('module_name')
    class_name = args.pop('class_name')
    for r in register:
        if [module_name, class_name, args] == r[:3]: return r[3]
    temp = __import__(module_name, globals(), locals(), [class_name], -1)
    c = getattr(temp, class_name)
    result = c(**args)
    register.append([module_name, class_name, args, result])
    return result
        