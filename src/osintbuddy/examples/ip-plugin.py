from osintbuddy.plugins import Plugin
import socket

# @todo


class IpPlugin(Plugin):
    def __init__(self):
        self.transforms = {
            "geolocate": self.get_location
        }
        self.node_name = "IP Address"
        self.node_inputs = [
            {
                "placeholder": "...",
                "name": "input-name",
                "icon": "some-tabler-icon class",
                "type": str
            }
        ]

    def get_location(self, ip: str):
        return socket.getaddrinfo(ip)
