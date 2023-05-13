class OBPluginError(Exception):
    pass


class NodeInvalidValueError(OBPluginError):
    pass


class NodeMissingValueError(OBPluginError):
    pass
