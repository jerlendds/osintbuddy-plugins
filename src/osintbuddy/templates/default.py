def plugin_source_template(label: str, description: str, author: str) -> str:
    class_name = ''.join(x for x in filter(str.isalnum, label.title()) if not x.isspace())

    return f"""import osintbuddy as ob
from osintbuddy.elements import TextInput

class {class_name}(ob.Plugin):
    label = '{label}'
    icon = 'atom-2'   # https://tabler-icons.io/
    color = '#FFD166'

    author = '{author}'
    description = '{description}'

    node = [
        TextInput(label='Example', icon='radioactive')
    ]

    @ob.transform(label='To example', icon='atom-2')
    async def transform_example(self, node, use):
        WebsitePlugin = await ob.Registry.get_plugin('website')
        website_plugin = WebsitePlugin()
        return website_plugin.blueprint(domain=node.example)
"""

