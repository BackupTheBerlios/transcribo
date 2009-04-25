# Transcribo


"""Styles for frames, ContentManagers and such like."""

translators = dict(
    yabt2 = dict(
        module_name = 'translator',
        class_name = 'YABTrans',
        state = 2
    ),
    upper = dict(
        module_name = 'translator',
        class_name = 'UpperTrans'
    )
)



wrappers = dict(
    indent2 = dict(
        module_name = 'textwrap',
        class_name = 'TextWrapper',
        initial_indent = '  '
    ),
    simple = dict(
        module_name = 'textwrap',
        class_name = 'TextWrapper'
    )
)


content = dict(
    default = dict(),
    heading1 = dict(
        x_align = 'center'
    ),
    heading2 = dict(x_align = 'left'),
    body1 = dict()
)



frames = dict(
    body1 = dict(
        x_align = 'left',
        x_hook = 'left',
        x_offset = 0,
        y_align ='top',
        y_hook = 'bottom',
        y_offset = 0,
        right_indent = 0,
        lines_below = 0,
        max_width = 0,
        width_mode = 'fixed',
        max_height = 0,
        height_mode = 'auto'
    ),
    heading1 = dict(
        x_align = 'left',
        x_hook = 'left',
        x_offset = 0,
        y_align ='top',
        y_hook = 'bottom',
        y_offset = 3,
        right_indent = 0,
        lines_below = 1,
        max_width = 0,
        width_mode = 'fixed',
        max_height = 0,
        height_mode = 'auto'
    ),
    heading2 = dict(
        x_align = 'left',
        x_hook = 'left',
        x_offset = 2,
        y_align ='top',
        y_hook = 'bottom',
        y_offset = 3,
        right_indent = 0,
        lines_below = 1,
        max_width = 0,
        width_mode = 'fixed',
        max_height = 0,
        height_mode = 'auto'
    ),
    heading3 = dict(
        x_align = 'left',
        x_hook = 'left',
        x_offset = 4,
        y_align ='top',
        y_hook = 'bottom',
        y_offset = 3,
        right_indent = 0,
        lines_below = 1,
        max_width = 0,
        width_mode = 'fixed',
        max_height = 0,
        height_mode = 'auto'
    ),
    list_container = dict(
        x_align = 'left',
        x_hook = 'left',
        x_offset = 0,
        y_align ='top',
        y_hook = 'top',
        y_offset = 0,
        right_indent = 0,
        lines_below = 0,
        max_width = 0,
        width_mode = 'fixed',
        max_height = 0,
        height_mode = 'auto'
    ),
    list_body = dict(
        x_hook = 'right',
        x_offset = 3,
        y_hook = 'bottom',
        y_offset = 0
    ),
    list_item_container = dict(
        x_align = 'left',
        x_hook = 'leftt',
        x_offset = 0,
        y_align ='top',
        y_hook = 'top',
        y_offset = 0,
        right_indent = 0,
        lines_below = 0,
        max_width = 0,
        width_mode = 'fixed',
        max_height = 0,
        height_mode = 'auto'
    ),
    list_item = dict(
        x_align = 'left',
        x_hook = 'leftt',
        x_offset = 0,
        y_align ='top',
        y_hook = 'top',
        y_offset = 0,
        right_indent = 0,
        lines_below = 0,
        max_width = 0,
        width_mode = 'auto',
        max_height = 1,
        height_mode = 'fixed'
    )
)

frames['default_heading'] = frames['heading3']



ContentMan = dict(
    body1_indent = dict(
        wrapper = wrappers['simple']
    ),
    body1 = dict(
        wrapper = wrappers['simple']
    ),
    heading1 = dict(
        align = 'center',
        translator = translators['upper'],
        wrapper = wrappers['simple']
    )
)


BulletSymbols = ['-', '-', '+', '*']

# map docutils nodes to styles. Used by getFrame()

frame = dict(
    body1 = frames['body1'],
    heading1 = frames['heading1'],
    heading2 = frames['heading2'],
    heading3 = frames['heading3'],
    default_heading = frames['heading3'],
    default = frames['body1'],
    list_container = frames['list_container'],
    list_item = frames['list_item'],
    list_body = frames['list_body'],
    list_item_container = frames['list_item_container']
)

translator = dict(yabt2 = translators['yabt2'], default = None, heading1 = translators['upper'], body1 = None, heading2 = None)