

from content import ContentManager
from frames import Frame

styles = {}


def getContentManager(cur, style = ''):
    '''
    return a content.ContentManager instance with the
    specified style (defaults to '').
    
    'cur'': the current frame in which the ContentManager will be placed
    
    'style': a string of words defining the styles of wrapper, translator and hyphenator.
    Example: style = 'wrapper indent2 translator upper hyphenator en_U'
    The order of the commands in the string does not matter. Separators except for white space are
    not allowed.
    '''
    

    # Prepare the style string for rudimentary parsing:
    words = style.split()
    
    # Choose the wrapper
    try:
        i = words.index('wrapper')
        wrapper_name = words[i + 1]
    except ValueError:
        wrapper_name = 'default'
        
    # Choose the translator
    try:
        i = words.index('translator')
        translator_name = words[i + 1]
    except ValueError:
        translator_name = 'default'
        
        
    # Choose the hyphenator
    try:
        i = words.index('hyphenator')
        hyphenator_name = words[i + 1]
    except ValueError:
        hyphenator_name = 'default'

    # Get the corresponding styles
    wrapper_style = styles['wrapper'][wrapper_name]
    translator_style = styles['translator'][translator_name]
    hyphenator_style = styles['hyphenator'][hyphenator_name]
        
    return ContentManager(parent = cur, wrapper = wrapper_style,
    hyphenator = hyphenator_style,
        translator = translator_style)


def getFrame(cur, par, style = 'default'):
    '''
    return a frames.Frame instance of the specified style.
    
    'cur': the current Frame
    'par': the parent frame of the one to be created
    'style': the name of a frame style (see the examples in the ./styles/ subdir)
    '''
    
    frame_style = styles['frame'][style]
    
    if par == cur:
        frame_style.update(y_hook = 'top')
    else:
        frame_style.update(y_hook = 'bottom')

    return Frame(parent = par,
        x_anchor = par, y_anchor = cur,
        **frame_style)

    
    