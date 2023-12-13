class BaseElement(object):
    """
    The BaseElement class represents a basic building block used in OsintBuddy
    plugins. It is designed to implement the base styles used
    in other nodes that can render a nodes element
    with a specific element type, label, and style on the OSINTbuddy UI.

    label : str
        A string representing the label for the node.
    style : dict
        A dictionary representing the react style properties for the node.
    placeholder : str
        A string representing the placeholder for the node.

    _base_blueprint(self) -> dict:
        Returns a dictionary containing essential data for a node
        element type, such as the node type, label,
        placeholder, and style.
    """
    def __init__(self, **kwargs):
        self.label: str = ''
        if entity_type := kwargs.get('label'):
            setattr(self, 'label', entity_type)

    def _base_entity_element(self, **kwargs):
        base_element = {}
        if kwargs:
            base_element = {
                k: v for k, v in kwargs.items()
            }
        base_element['label'] = self.label
        base_element['type'] = self.element_type
        return base_element

class BaseInput(BaseElement):
    pass


class BaseDisplay(BaseElement):
    pass
