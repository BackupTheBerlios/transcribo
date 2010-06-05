

ffrom transcribo.renderer import styles

def getContentManager(content_style = 'default', translator_style = None, wrapper_style = 'default',
    hyphenator_style = 'hyphen_en_US'):
    if not translator_style:
        translator_style = self.settings.translator        translator_cfg = styles['translators'][translator_style]
    try:
        content_cfg = styles['content'][content_style]
    except KeyError:
        content_cfg = styles['content']['standard']
    try:
        wrapper_cfg = styles['wrappers'][wrapper_style]
    except KeyError:
        wrapper_cfg = styles['wrappers']['standard']
    if hyphenator_style:
        hyphenator_cfg = styles['hyphenators'][hyphenator_style]
    else: hyphenator_cfg = None
    return ContentManager(parent = self.currentFrame, wrapper = wrapper_cfg,
    hyphenator = hyphenator_cfg,
        translator = translator_cfg,
        **content_cfg)


def getFrame(self, style):
    frame_cfg = styles['frames'][style]
    result = Frame(parent = self.parent,
    x_anchor = self.parent, y_anchor = self.currentFrame,
    **frame_cfg)
    if self.parent == self.currentFrame:
        result.update(y_hook = 'top')
    else:
        result.update(y_hook = 'bottom')
    return result
    
    