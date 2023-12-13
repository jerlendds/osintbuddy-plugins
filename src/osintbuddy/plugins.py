import os, imp, importlib, inspect
from typing import List, Any, Callable
from collections import defaultdict
from pydantic import BaseModel, ConfigDict
from osintbuddy.elements.base import BaseElement
from osintbuddy.errors import OBPluginError
from osintbuddy.utils import to_snake_case


OBNodeConfig = ConfigDict(extra="allow", frozen=False, populate_by_name=True, arbitrary_types_allowed=True)

class OBNode(BaseModel):
    model_config = OBNodeConfig


def plugin_results_middleman(f):
    def return_result(r):
        return r
    def yield_result(r):
        for i in r:
            yield i
    def decorator(*a, **kwa):
        if inspect.isgeneratorfunction(f):
            return yield_result(f(*a, **kwa))
        else:
            return return_result(f(*a, **kwa))
    return decorator


class OBAuthorUse(BaseModel):
    get_driver: Callable[[], None]


class OBRegistry(type):
    plugins = []
    labels = []
    ui_labels = []

    def __init__(cls, name, bases, attrs):
        """
        Initializes the OBRegistry metaclass by adding the plugin class
        and its label if it is a valid plugin.
        """
        if name != 'OBPlugin' and name != 'Plugin' and issubclass(cls, OBPlugin):
            label = cls.label.strip()
            if cls.show_label is True:
                if isinstance(cls.author, list):
                    cls.author = ', '.join(cls.author)
                OBRegistry.ui_labels.append({
                    'label': label,
                    'description': cls.description,
                    'author': cls.author
                })
            OBRegistry.labels.append(label)
            OBRegistry.plugins.append(cls)

    @classmethod
    async def get_plugin(cls, plugin_label: str):
        """
        Returns the corresponding plugin class for a given plugin_label or
        'None' if not found.

        :param plugin_label: The label of the plugin to be returned.
        :return: The plugin class or None if not found.
        """
        for idx, label in enumerate(cls.labels):
            if label == plugin_label or to_snake_case(label) == to_snake_case(plugin_label):
                return cls.plugins[idx]
        return None

    @classmethod
    def get_plug(cls, plugin_label: str):
        """
        Returns the corresponding plugin class for a given plugin_label or
        'None' if not found.

        :param plugin_label: The label of the plugin to be returned.
        :return: The plugin class or None if not found.
        """
        for idx, label in enumerate(cls.labels):
            if to_snake_case(label) == to_snake_case(plugin_label):
                return cls.plugins[idx]
        return None

    def __getitem__(self, i: str):
        return self.get_plug[i]

# https://stackoverflow.com/a/7548190
def load_plugin(
    mod_name: str,
    plugin_code: str,
):
    """
    Load plugins from a string of code

    :param module_name: The desired module name of the plugin.
    :param plugin_code: The code of the plugin.
    :return:
    """
    new_mod = imp.new_module(mod_name)
    exec(plugin_code, new_mod.__dict__)
    return OBRegistry.plugins


def load_plugins(
    entities: list
):
    """
    Loads plugins from the osintbuddy db

    :param entities: list of entities from the db
    :return:
    """
    for entity in entities:
        mod_name = to_snake_case(entity.label)
        new_mod = imp.new_module(mod_name)
        exec(entity.source, new_mod.__dict__)
    return OBRegistry.plugins


def discover_plugins(
    dir_path: str = '/plugins.osintbuddy.com/src/osintbuddy/core/',
):
    """
    Scans the specified 'dir_path' for '.py' files, imports them as plugins,
    and populates the OBRegistry with classes.

    :param dir_path: The directory path where the plugins are located.
    :return: List of plugin classes
    """
    for r, _, files in os.walk(dir_path):
        for filename in files:
            modname, ext = os.path.splitext(filename)
            if ext == '.py':
                try:
                    modpath = r.replace("/app/", "")
                    if 'osintbuddy/core' in dir_path:
                        modpath = r.replace("/plugins.osintbuddy.com/src/", "")
                    modpath = modpath.replace("/", ".")
                    importlib.import_module(f'{modpath}{modname}')
                except ImportError as e:
                    print(f"Error importing plugin '{modpath}{modname}': {e}")

    return OBRegistry.plugins


def transform(label, icon='list', edge_label='transformed_to'):
    """
    A decorator add transforms to an osintbuddy plugin.

    Usage:
    @transform(label=<label_text>, icon=<tabler_react_icon_name>)
    def transform_to_ip(self, node, **kwargs):
        # Method implementation

    :param label: str, A string representing the label for the transform
        method, which can be utilized for displaying in the context menu.
    :param icon: str, Optional icon name, representing the icon associated
        displayed by the transform label. Default is "list".
    :return: A decorator for the plugin transform method.
    """
    def decorator_transform(func, edge_label=edge_label):
        async def wrapper(self, node, **kwargs):
            return await func(self=self, node=node, **kwargs)
        wrapper.label = label
        wrapper.icon = icon
        wrapper.edge_label = edge_label
        return wrapper
    return decorator_transform


class OBPlugin(object, metaclass=OBRegistry):
    """
    OBPlugin is the base class for all plugin classes in this application.
    It provides the required structure and methods for a plugin.
    """
    entity: List[BaseElement]
    color: str = '#145070'
    label: str = ''
    icon: str = 'atom-2'
    show_label = True

    author = 'Unknown'
    description = 'No description.'

    def __init__(self):
        transforms = self.__class__.__dict__.values()
        self.transforms = {
            to_snake_case(func.label): func for func in transforms if hasattr(func, 'label')
        }
        self.transform_labels = [
            {
                'label': func.label,
                'icon': func.icon,
            } for func in transforms
            if hasattr(func, 'icon') and hasattr(func, 'label')
        ]

    def __call__(self):
        return self.blueprint()

    @staticmethod
    def _map_graph_data_labels(element, **kwargs):
        label = to_snake_case(element['label'])
        for element_key in kwargs.keys():
            if element_key == label:
                if isinstance(kwargs[label], str):
                    element['value'] = kwargs[label]
                elif isinstance(kwargs[label], dict):
                    for t in kwargs[label]:
                        element[t] = kwargs[label][t]
        return element

    @classmethod
    def blueprint(cls, **kwargs):
        """
        Generate and return a dictionary representing the plugins node.
        Includes label, name, color, icon, and a list of all elements
        for the node/plugin.
        """
        entity_ui_node = defaultdict(None)
        entity_ui_node['label'] = cls.label
        entity_ui_node['color'] = cls.color if cls.color else '#145070'
        entity_ui_node['icon'] = cls.icon
        entity_ui_node['elements'] = []
        if cls.entity:
            for element in cls.entity:
                # if an entity element is a nested list, 
                # elements will be positioned next to each other horizontally
                if isinstance(element, list):
                    entity_ui_node['elements'].append([
                        cls._map_graph_data_labels(elm.to_dict(), **kwargs)
                        for elm in element
                    ])
                # otherwise position the entity elements vertically on the actual UI entity node
                else:
                    element_row = cls._map_graph_data_labels(element.to_dict(), **kwargs)
                    entity_ui_node['elements'].append(element_row)
            return entity_ui_node
        if cls.node:
            print("WARNING! Using node in plugins is being deprecated! Please switch to entity = [TextInput(...), ...] ")
            for element in cls.node:
                # if an entity element is a nested list, 
                # elements will be positioned next to each other horizontally
                if isinstance(element, list):
                    row_elms = []
                    for elm in element:
                        row_elms.append(cls._map_graph_data_labels(elm.to_dict(), **kwargs))
                    entity_ui_node['elements'].append(row_elms)
                # otherwise position the entity elements vertically on the actual UI entity node
                else:
                    element_row = cls._map_graph_data_labels(element.to_dict(), **kwargs)
                    entity_ui_node['elements'].append(element_row)
            return entity_ui_node


    async def get_transform(self, transform_type: str, entity, use: OBAuthorUse) -> Any:
        """ Return output from a function accepting node data.
            The function will be called with a single argument, the node data
            from when a node context menu action is taken - and should return
            a list of Nodes.
            None if the plugin doesn't provide a transform
            for the transform_type.
        """
        transform_type = to_snake_case(transform_type)
        if self.transforms and self.transforms[transform_type]:
            try:
                transform = await self.transforms[transform_type](
                    self=self,
                    node=self._map_to_transform_data(entity),
                    use=use
                )
                edge_label = self.transforms[transform_type].edge_label
                if not isinstance(transform, list):
                    transform['edge_label'] = edge_label
                    return [transform]
                [
                    n.__setitem__('edge_label', edge_label)
                    for n in transform
                ]
                return transform
            except (Exception, OBPluginError) as e:
                if isinstance(e, OBPluginError):
                    raise OBPluginError(e)
                raise OBPluginError(f'This plugin has run into an unhandled error: {e}')
        return None

    @staticmethod
    def _map_element(transform_map: dict, element: dict):
        label = to_snake_case(element.pop('label', None))
        transform_map[label] = {}
        element_type = element.pop('type', None)
        element.pop('icon', None)
        element.pop('placeholder', None)
        element.pop('style', None)
        element.pop('options', None)
        for k, v in element.items():
            if (isinstance(v, str) and len(element.values()) == 1) or element_type == 'dropdown':
                transform_map[label] = v
            else:
                transform_map[label][k] = v

    @classmethod
    def _map_to_transform_data(cls, node: dict) -> OBNode:
        transform_map: dict = {}
        data: dict = node.get('data', {})
        elements: list[dict] = data.get('elements', [])
        for element in elements:
            if isinstance(element, list):
                [cls._map_element(transform_map, elm) for elm in element]
            else:
                cls._map_element(transform_map, element)
        return OBNode(**transform_map)
