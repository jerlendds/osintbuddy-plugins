#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
from __future__ import annotations
from osintbuddy import OBRegistry, OBPlugin, transform, discover_plugins
from osintbuddy.node import TextInput


# Mock
def test_ob_registry():
    assert OBRegistry.plugins == []
