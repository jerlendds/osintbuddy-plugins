from typing import List, Any
from osintbuddy.elements.base import BaseInput


class UploadFileInput(BaseInput):
    """
    The UploadFileInput class represents an upload file input node used
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
    node_type: str = "upload"

    def __init__(self, value="", supported_files=[], icon="IconFileUpload", **kwargs):
        super().__init__(**kwargs)
        self.value: Any = value
        self.icon: str = icon
        self.supported_files: List[str] = supported_files

    def json(self):
        node = self._base_blueprint()
        node["value"] = self.value
        node["icon"] = self.icon
        node["supported_files"] = self.supported_files
        return node


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
    node_type: str = "text"

    def __init__(self, value="", default="", icon="IconAlphabetLatin", **kwargs):
        super().__init__(**kwargs)
        self.value: str = value
        self.icon: str = icon

    def json(self):
        node = self._base_blueprint()
        node["value"] = self.value
        node["icon"] = self.icon
        return node


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
    node_type: str = "dropdown"

    def __init__(self, options=[], value={'label': '', 'tooltip': '', 'value': ''}, **kwargs):
        super().__init__(**kwargs)
        self.options: List[any] = options
        self.value: dict = value

    def json(self):
        node = self._base_blueprint()
        node["options"] = self.options
        node["value"] = self.value
        return node


class NumberInput(BaseInput):
    """
    The NumberInput class represents a whole number input node used
    in the OsintBuddy plugin system.

    value : int
        The integer value stored in the node.

    Usage Example:
    class Plugin(OBPlugin):
        node = [NumberInput(value=10, placeholder='Enter a whole number')]
    """
    node_type: str = "number"

    def __init__(self, value=1, icon="123", **kwargs):
        super().__init__(**kwargs)
        self.value: int = value
        self.icon = icon

    def json(self):
        node = self._base_blueprint()
        node["value"] = self.value
        node["icon"] = self.icon
        return node


class DecimalInput(BaseInput):
    """
    The DecimalInput class represents a decimal number input node used
    in the OsintBuddy plugin system.
    value : float
        The float value stored in the node.

    Usage Example:
    class Plugin(OBPlugin):
        node = [DecimalInput(value=3.14, placeholder='Enter a decimal number')]
    """
    node_type: str = "decimal"

    def __init__(self, value=3.14, icon="123", **kwargs):
        super().__init__(**kwargs)
        self.value: float = value
        self.icon = icon

    def json(self):
        node = self._base_blueprint()
        node["value"] = self.value
        node["icon"] = self.icon
        return node
