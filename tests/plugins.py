from osintbuddy import OBPlugin, transform
from osintbuddy.node import TextInput

class WebsitePlugin(OBPlugin):
    label = 'Website'
    name = 'Website'
    color = '#1D1DB8'
    icon = 'world-www'
    node = [
        TextInput(label='Domain', icon='world-www'),
    ]


class UrlPlugin(OBPlugin):
    label = 'URL'
    name = 'URL'
    color = '#642CA9'
    node = [
        TextInput(label='URL', icon='link'),
    ]

    @transform(label='To website', icon='world-www')
    def transform_to_website(self, node, **kwargs):
        return WebsitePlugin.blueprint(domain='google.com')

