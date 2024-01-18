import os, imp, importlib, inspect, sys
from types import ModuleType
from typing import List, Any, Callable
from collections import defaultdict
from pydantic import BaseModel, ConfigDict
from osintbuddy.elements.base import BaseElement
from osintbuddy.errors import OBPluginError
from osintbuddy.utils import to_snake_case


IcgNodeConfig = ConfigDict(extra="allow", frozen=False, populate_by_name=True, arbitrary_types_allowed=True)

class EntityProperties(BaseModel):
    source_entity: str
    model_config = IcgNodeConfig


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


class TransformUse(BaseModel):
    get_driver: Callable[[], None]

# https://stackoverflow.com/a/7548190
def load_plugin_source(
    mod: ModuleType,
    plugin_code: str,
) -> ModuleType:
    """
    Load plugins from a string of code

    :param module_name: The desired module name of the plugin.
    :param plugin_code: The code of the plugin.
    :return:
    """    
    if isinstance(mod, str):
        mod = imp.new_module(mod)
    exec(plugin_code, mod.__dict__)
    return mod


class EntityRegistry(type):
    entities = []
    _labels = []
    _visible_entities = []

    def __init__(cls, name, bases, attrs):
        """
        Initializes the OBRegistry metaclass by adding the plugin class
        and its label if it is a valid plugin.
        """
        if name != 'DiscoverableEntity' and issubclass(cls, DiscoverableEntity):
            label = cls.label.strip()
            if isinstance(cls.author, list):
                cls.author = ', '.join(cls.author)
            if cls.show_label is True:
                EntityRegistry._visible_entities.append({
                    'label': label,
                    'description': cls.description,
                    'author': cls.author
                })
            EntityRegistry._labels.append(label)
            EntityRegistry.entities.append(cls)

    @classmethod
    async def get_plugin(cls, plugin_label: str):
        """
        Returns the corresponding plugin class for a given plugin_label or
        'None' if not found.

        :param plugin_label: The label of the plugin to be returned.
        :return: The plugin class or None if not found.
        """
        for entity in cls.entities:
            if entity.label == plugin_label or to_snake_case(entity.label) == to_snake_case(plugin_label):
                return entity

    @classmethod
    def _get_plugin(cls, plugin_label: str):
        """
        Returns the corresponding plugin class for a given plugin_label or
        'None' if not found.

        :param plugin_label: The label of the plugin to be returned.
        :return: The plugin class or None if not found.
        """
        for entity in cls.entities:
            if entity.label == plugin_label or to_snake_case(entity.label) == to_snake_case(plugin_label):
                return entity

    def __getitem__(self, i: str):
        return self._get_plugin[i]

    @staticmethod
    def load_db_plugins(
        entities: list,
        mod_name: str = None
    ):
        """
        Loads plugins from the osintbuddy db

        :param entities: list of entities from the db
        :return:
        """
        if mod_name is not None:
            mod = imp.new_module(mod_name) 
        for entity in entities:
            if mod_name is None:
                mod = imp.new_module(to_snake_case(entity.label))
            load_plugin_source(mod, entity.source)

    @staticmethod
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

        return EntityRegistry.entities


def transform(label, icon='transform', edge_label='has_result'):
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
        async def wrapper(self, context, **kwargs):
            return await func(self, context, **kwargs)
        wrapper.label = label
        wrapper.icon = icon
        wrapper.edge_label = edge_label
        return wrapper
    return decorator_transform


def register_transform(entity_class, label, icon='transform', edge_label='has_result'):
    """
    TODO: Document me
    """
    def decorator_transform(func, edge_label=edge_label):
        async def wrapper(context, **kwargs):
            return await func(context, **kwargs)
        func.label = label
        func.icon = icon
        func.edge_label = edge_label
        setattr(entity_class, func.__name__, func)
        return wrapper
    return decorator_transform


class DiscoverableEntity(object, metaclass=EntityRegistry):
    """
    OBPlugin is the base class for all plugin classes in this application.
    It provides the required structure and methods for a plugin.
    """
    properties: List[BaseElement] = []
    color: str = '#145070'
    label: str = ''
    icon: str = 'transform'
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

    def __call__(self, **kwargs):
        return self.create(**kwargs)

    @staticmethod
    def _build_entity_properties(element, **properties):
        label = to_snake_case(element['label'])
        for element_key in properties.keys():
            if element_key == label:
                if isinstance(properties[label], str):
                    element['value'] = properties[label]
                elif isinstance(properties[label], dict):
                    for t in properties[label]:
                        element[t] = properties[label][t]
        return element

    @classmethod
    def create(cls, **data_properties):
        """
        Generate and return a dictionary representing the entity as seen on the ui.
        """
        if not cls.properties:
            raise NotImplementedError((
                "No entity_properties found."
                "Entity properties must exist for a DiscoverableEntity"
            ))
        node = defaultdict(None)
        node['label'] = cls.label
        node['color'] = cls.color if cls.color else '#145070'
        node['icon'] = cls.icon
        node['elements'] = []
        for element in cls.properties:
            # if an entity element is a nested list, 
            # elements will be positioned next to each other horizontally
            if isinstance(element, list):
                row_elms = []
                for elm in element:
                    row_elms.append(cls._build_entity_properties(elm.to_dict(), **data_properties))
                node['elements'].append(row_elms)
            # otherwise position the entity elements vertically on the actual UI entity 
            # (elements aka properties can be viewed after double clicking an entity on the graph UI,
            # this toggles that entity into edit mode displaying these elements we are building here)
            else:
                element_row = cls._build_entity_properties(element.to_dict(), **data_properties)
                node['elements'].append(element_row)
        return node

    async def run_transform(self, transform_type: str, transform_context: dict, use: TransformUse) -> Any:
        """ Return output from a function accepting node data.
            The function will be called with a single argument, the node data
            from when a node context menu action is taken - and should return
            a list of Nodes.
            None if the plugin doesn't provide a transform
            for the transform_type.
        """
        transform_type = to_snake_case(transform_type)
        if transform_func := self.transforms.get(transform_type):
            transform = await transform_func(
                self=self,
                context=self._map_to_transform_context(transform_context),
                use=use
            )
            edge_label = transform_func.edge_label
            if not isinstance(transform, list):
                transform['edge_label'] = edge_label
                return [transform]
            [
                n.__setitem__('edge_label', edge_label)
                for n in transform
            ]
            return transform
        return None

    @staticmethod
    def _map_element(transform_map: dict, element: dict):
        label = to_snake_case(element.pop('label', None))
        transform_map[label] = {}
        element_type = element.pop('type', None)
        element.pop('icon', None)
        element.pop('placeholder', None)
        element.pop('options', None)
        for k, v in element.items():
            if (isinstance(v, str) and len(element.values()) == 1) or element_type == 'dropdown':
                transform_map[label] = v
            else:
                transform_map[label][k] = v

    @classmethod
    def _map_to_transform_context(cls, entity_context: dict) -> EntityProperties:
        transform_map: dict = {}
        data: dict = entity_context.get('data', {})
        entity_type = entity_context.get("data", {}).get("label")
        elements: list[dict] = data.get('elements', [])
        for element in elements:
            if isinstance(element, list):
                [cls._map_element(transform_map, elm) for elm in element]
            else:
                cls._map_element(transform_map, element)
        return EntityProperties(source_entity=entity_type, **transform_map)
