def plugin_source_template(label: str, description: str, author: str) -> str:
    class_name = ''.join(x for x in filter(str.isalnum, label.title()) if not x.isspace())

    return f'''from osintbuddy import DiscoverableEntity, transform
from osintbuddy.elements.inputs import TextInput

class {class_name}(ob.DiscoverableEntity):
    label = "{label}"
    icon = "face-id"   # https://tabler-icons.io/
    color = "#08ba73cc"

    properties = [
        TextInput(label='Example', icon='command')
    ]

    author = "{author}"
    description = "{description}"

    @transform(label="To Website Example", icon="transform")
    async def transform_example(self, node, use):
        website_entity = await ob.Registry.get_plugin('website')
        return website_entity.create(domain=node.example)
'''

