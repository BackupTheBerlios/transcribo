# Transcribo


"""Styles for frames, ContentManagers and such like."""


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


frames = dict(
    body1 = dict(
        x_align = 'left',
        x_hook = 'left',
        x_offset = 0,
        y_align ='top',
        y_hook = 'bottom',
        y_offset = 1,
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
    )
)

ContentMan = dict(
    body1_indent = dict(
        wrapper = wrappers['indent2']
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



# map docutils nodes to styles

frame = dict(
    normal = frames['body1'],
    normal0 = frames['body1'],
    default = frames['body1']
)

translator = dict(default = translators['yabt2'])
