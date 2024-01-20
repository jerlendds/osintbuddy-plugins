# OSINTBuddy plugins and extensions

The plugins library for [jerlendds/osintbuddy](https://github.com/jerlendds/osintbuddy). Currently in beta, expect changes to come...

***Please note:** [OSINTBuddy plugins](https://github.com/jerlendds/osintbuddy-plugins) are still in early alpha and breaking changes may occasionally occur in the API. That said, if you remain on the `main` branch and avoid accessing protected methods we will try our best to avoid introducing breaking changes.*

- **NOTICE:** There has been a major update to plugins, any created plugins will have to be updated.
    - Please see the introduction to the plugin system below


The osintbuddy plugin system at its core is very simple. An `OBRegistry` class holds all registered `OBPlugin` classes within the application. This registry is loaded into the [osintbuddy application](https://github.com/jerlendds/osintbuddy/) where it is then used to load the available entities for the user when they access a project graph, load transforms when a user opens the context menu of a node, and perform transformations which expect a `Plugin.blueprint()` to be returned. The returned data of a transform decorated method will be automatically mapped to a [JanusGraph](https://janusgraph.org/) database through [gremlin](https://tinkerpop.apache.org/) according to the labels *(as snakecase)* you previously set in the classes `node` for whatever `Plugin.blueprint()`
you return.
 
To make this a bit more clear please see the below example...

```py
from pydantic import BaseModel
import osintbuddy import transform, DiscoverableEntity
from osintbuddy.elements import TextInput, DropdownInput, Title, CopyText
from osintbuddy.errors import OBPluginError


class CSESearchResults(DiscoverableEntity):
    label = "Google CSE Result"
    # do not show this on the entities dialog 
    # the user sees on the left of the project graph screen
    show_label = False 
    color = "#058F63"
    # Properties displayed while in entity edit mode on the
    # osintbuddy graph UI
    properties = [
        Title(label="Result"),
        CopyText(label="URL"),
        CopyText(label="Cache URL"),
    ]


class CSESearchPlugin(DiscoverableEntity):
    label = "Google CSE Search"
    color = "#2C7237"
    properties = [
        [
            TextInput(label="Query", icon="search"),
            TextInput(label="Pages", icon="123", default="1"),
        ],
        DropdownInput(label="CSE Categories", options=cse_link_options)
    ]

    @transform(label="To cse results", icon="search")
    async def transform_to_cse_results(
      self,
      # context: dynamically generated pydantic model 
      # that is mapped from the above labels (note the `properties = [...]`) contained within `context`
      context: BaseModel, 
      # use: a pydantic model allowing you to access a selenium instance
      # (and eventually more...!) 
      use
    ):
        results = []

        if not context.query:
          raise OBPluginError((
            'You can send error messages to the user here'
            'if they forget to submit data or if some other error occurs'
          ))

        if not context.cse_categories:
            raise OBPluginError('The CSE Category field is required to transform.')

        # notice how you can access data returned from the context menu
        # of this node; using the label name in snake case
        print(context.cse_categories, context.query, context.pages) 

        ... # (removed code for clarity)
        response = await self.get_cse_results(context.query, context.cse_categories, context.max_results)

        if response:
            cse_result_entity = await EntityRegistry.get_plugin("google_cse_result")
            for result in response["results"]:
                url = result.get("breadcrumbUrl", {})
                # some elements you can store more than just a string,
                # (these elements storing dicts are mapped 
                # to janusgraph as properties with the names
                # result_title, result_subtitle, and result_text)
                ui_entity = cse_result_entity.create(
                    result={
                        "title": result.get("titleNoFormatting"),
                        "subtitle": url.get("host") + url.get("crumbs"),
                        "text": result.get("contentNoFormatting"),
                    },
                    url=result.get("unescapedUrl"),
                    cache_url=result.get("cacheUrl"),
                )
                results.append(ui_entity)
        # here we return a list of blueprints (blueprints are dicts)
        # but you can also return a single blueprint without a list
        return results

    async def get_cse_results(self, query, url, max_results=100):
        ...
```

        

