[![Total Downloads](https://static.pepy.tech/badge/osintbuddy)](https://pepy.tech/project/osintbuddy)
[![Downloads](https://static.pepy.tech/badge/osintbuddy/week)](https://pepy.tech/project/osintbuddy)

# OSINTBuddy plugins

The plugins library for [jerlendds/osintbuddy](https://github.com/jerlendds/osintbuddy), coming soon...
![osintbuddy-demo](https://github.com/jerlendds/osintbuddy/assets/29207058/c01357a9-9e55-44e3-9734-c84130bd110b)

This project follows the Python Standards declared in PEP 621. It uses a pyproject.yaml file to configure the project and Flit to simplify the build process and publish to PyPI.

## Extending OSINTBuddy with plugins

The OsintBuddy API provides an easy way to create and extend plugins in a modular manner. In the given code example, the IPAddressPlugin is created as an extension to the OsintBuddy framework using the OBPlugin class. This IP address plugin has the following features:

1. Customizable plugin attributes such as label, name, and color.
2. A node definition for user input, in this case, a TextInput for IP addresses.
3. A transform method (transform_to_website) with a specified label and icon. This method can take the input data (an IP address) and convert it to a different format, like a website.
4. Error handling capabilities using the OBPluginError class if an issue occurs during data transformation.

The extensible nature of the OsintBuddy API allows developers to seamlessly integrate custom plugins such as an IPAddressPlugin into their applications and workflows, simplifying the process of transforming and manipulating data across various formats. 
Not shown here is also the ability to access a selenium driver context with `kwargs['get_driver']()`

```py
from osintbuddy.plugins import OBPlugin
from osintbuddy.node import TextInput

class IPAddressPlugin(OBPlugin):
    label = 'IP'
    name = 'IP address'
    color = '#F47C00'
    node = [
        TextInput(label='IP Address', icon='map-pin')  # tabler-icon names
    ]

    @transform(label='To website', icon='world', prompt="""""")
    def transform_to_website(self, node, **kwargs):
        try:
            resolved = socket.gethostbyaddr(node['data'][0])
            if len(resolved) >= 1:
                blueprint = WebsitePlugin.blueprint(domain=resolved[0])
                return blueprint
            else:
                raise OBPluginError('No results found')
        except (socket.gaierror, socket.herror):
            raise OBPluginError('We ran into a socket error. Please try again')
```

## Creating a plugin with dependent plugins

```py

class GoogleResult(OBPlugin):
    label = 'Google Result'
    show_label = False
    name = 'Google result'
    color = '#308e49'
    node = [
        Title(label='result'),
        CopyText(label='url')
    ]

    @transform(label='To website', icon='world')
    def transform_to_website(self, node, **kwargs):
        blueprint = WebsitePlugin.blueprint(
            domain=urlparse(node['data'][3]).netloc
        )
        return blueprint


class WebsitePlugin(OBPlugin):
    label = 'Website'
    name = 'Website'
    color = '#1D1DB8'
    icon = 'world-www'
    node = [
        TextInput(label='Domain', icon='world-www'),
    ]

    @transform(label='To google', icon='world')
    def transform_to_google(self, node, **kwargs):
        # @todo
        domain = node['data'][0]
        query = f"{domain}"
        results = []
        for result in GoogleSearchPlugin().search_google(query=query, pages="3"):
            blueprint = GoogleResult.blueprint(
                result={
                    'title': result.get('title'),
                    'subtitle': result.get('breadcrumb'),
                    'text': result.get('description'),
                },
                url=result.get('url')
            )
            results.append(blueprint)
        return results
```

GoogleResult holds information about a specific Google search result. It includes a transform_to_website method that appears on the UI context menu when you right click a GoogleResult node. When someone executes the transform the Google result information is sent to the transform where it's then turned into Website node after processing some of the sent data.

## Project Organization

- `.github/workflows`: Contains GitHub Actions used for building, testing, and publishing.
- `src`: source code
  - `src/node`: elements used to define a nodes appearance and input elements  
- `tests`: Contains Python-based test cases to validate source code.
- `pyproject.toml`: Contains metadata about the project and configurations for additional tools used to format, lint, type-check, and analyze Python code.


