from typing import List, Any
from osintbuddy.elements.base import BaseInput


class UploadFileInput(BaseInput):
    """
    !!WORK_IN_PROGRESS!! The UploadFileInput class represents an upload file input node used
    in the OsintBuddy plugin system.
    value : Any
        The initial value for the input node.
    icon : str
        The icon to be displayed with the node.
    supported_files : List[str]
        A list of supported file extensions for the node.

    Usage Example:
    class Plugin(OBPlugin):
        node = [UploadFileInput(supported_files=['.pdf', '.docx'])]
    """
    element_type: str = "upload"

    def __init__(self, value="", supported_files=[], icon="IconFileUpload", **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value,
            "icon": icon,
            "supported_files": supported_files,
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)


class TextInput(BaseInput):
    """The TextInput class represents a text input node used
    in the OsintBuddy plugin system.
    value : str
        The value stored in the element.
    icon : str
        The icon to be displayed with the input element.
    default : str
        The default value for the input element.

    Usage Example:
    class Plugin(OBPlugin):
        node = [TextInput(label='Email search', placeholder='Enter email')]
    """
    element_type: str = "text"

    def __init__(self, value="", default="", icon="IconAlphabetLatin", **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value,
            "icon": icon
        }
    def to_dict(self):
        return self._base_entity_element(**self.element)


class DropdownInput(BaseInput):
    """
    The DropdownInput class represents a dropdown menu node used
    in the OsintBuddy plugin system.
    options : List[any]
        A list of options for the dropdown menu.
    value : str
        The initially selected option in the dropdown menu.

    Usage Example:
    class Plugin(OBPlugin):
        node = [
            DropdownInput(
                options=[{'label': 'Option 1', 'tooltip': 'Hello on hover!'}],
                value='Option 1'
            )
        ]
    """
    element_type: str = "dropdown"

    def __init__(self, options=[], value={'label': '', 'tooltip': '', 'value': ''}, **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "options": options,
            "value": value
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)



class NumberInput(BaseInput):
    """
    !!WORK_IN_PROGRESS!! The NumberInput class represents a whole number input node used
    in the OsintBuddy plugin system.

    value : int
        The integer value stored in the node.

    Usage Example:
    class Plugin(OBPlugin):
        node = [NumberInput(value=10, placeholder='Enter a whole number')]
    """
    element_type: str = "number"

    def __init__(self, value=1, icon="123", **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value,
            "icon": icon
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)


class DecimalInput(BaseInput):
    """
    !!WORK_IN_PROGRESS!! The DecimalInput class represents a decimal number input node used
    in the OsintBuddy plugin system.
    value : float
        The float value stored in the node.

    Usage Example:
    class Plugin(OBPlugin):
        node = [DecimalInput(value=3.14, placeholder='Enter a decimal number')]
    """
    element_type: str = "decimal"

    def __init__(self, value=3.14, icon="123", **kwargs):
        super().__init__(**kwargs)
        self.element = {
            "value": value,
            "icon": icon
        }

    def to_dict(self):
        return self._base_entity_element(**self.element)

