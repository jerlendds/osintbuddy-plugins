from osintbuddy.elements.base import BaseDisplay


class Title(BaseDisplay):
    element_type: str = 'title'

    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value,
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)


class Text(BaseDisplay):
    element_type: str = 'section'

    def __init__(self, value='', icon="123", **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value,
            "icon": icon
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)


class Empty(BaseDisplay):
    element_type: str = 'empty'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()


class CopyText(BaseDisplay):
    element_type: str = 'copy-text'

    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)


class CopyCode(BaseDisplay):
    element_type: str = 'copy-code'

    def __init__(self, value='', **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)


class Json(BaseDisplay):
    element_type: str = 'json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()


class Image(BaseDisplay):
    element_type: str = 'image'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()


class Pdf(BaseDisplay):
    element_type: str = 'pdf'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()


class Video(BaseDisplay):
    element_type: str = 'video'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()


class List(BaseDisplay):
    element_type: str = 'list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()


class Table(BaseDisplay):
    element_type: str = 'table'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return self._base_entity_element()
