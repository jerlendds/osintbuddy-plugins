from osintbuddy.elements.base import BaseDisplay


class Title(BaseDisplay):
    node_type: str = 'title'

    def __init__(self, title='', subtitle='', text='', **kwargs):
        super().__init__(**kwargs)
        self.title: str = title
        self.subtitle: str = subtitle
        self.text: str = text

    def json(self):
        blueprint = self._base_blueprint()
        blueprint['title'] = self.title
        blueprint['subtitle'] = self.subtitle
        blueprint['text'] = self.text
        return blueprint


class Text(BaseDisplay):
    node_type: str = 'section'

    def __init__(self, value='', icon=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.icon = icon

    def json(self):
        blueprint = self._base_blueprint()
        blueprint['value'] = self.value
        blueprint['icon'] = self.icon
        return blueprint


class Empty(BaseDisplay):
    node_type: str = 'empty'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint


class CopyText(BaseDisplay):
    node_type: str = 'copy-text'

    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def json(self):
        blueprint = self._base_blueprint()
        blueprint['value'] = self.value
        return blueprint


class CopyCode(BaseDisplay):
    node_type: str = 'copy-code'

    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def json(self):
        blueprint = self._base_blueprint()
        blueprint['value'] = self.value
        return blueprint


class Json(BaseDisplay):
    node_type: str = 'json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint


class Image(BaseDisplay):
    node_type: str = 'image'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint


class Pdf(BaseDisplay):
    node_type: str = 'pdf'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint


class Video(BaseDisplay):
    node_type: str = 'video'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint


class List(BaseDisplay):
    node_type: str = 'list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint


class Table(BaseDisplay):
    node_type: str = 'table'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def json(self):
        blueprint = self._base_blueprint()
        return blueprint
