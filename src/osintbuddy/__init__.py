#   -------------------------------------------------------------
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""Python Package Template"""
from __future__ import annotations
from osintbuddy.plugins import (
    EntityRegistry,
    EntityRegistry as Registry,
    EntityPlugin,
    EntityPlugin as Plugin,  # TODO: log warning on use and deprecate me
    TransformCtx,
    TransformCtx as PluginUse,  # TODO: log warning on use and deprecate me
    discover_plugins,
    transform,
    load_local_plugin,
    load_local_plugins,
    register_transform
)

__version__ = "0.0.5"
