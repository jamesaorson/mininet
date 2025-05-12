from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom


# Topology to be instantiated in Mininet
class MNTopo(Topo):
    """Mininet test topology"""

    def __init__(self, cpu=0.1, max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        # Host and link configuration
        hostConfig = {"cpu": cpu}
        linkConfig = {
            "bw": 10,
            "delay": "1ms",
            "loss": 0,
            "max_queue_size": max_queue_size,
        }

        # Hosts and switches
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        s3 = self.addSwitch("s3")
        sender = self.addHost("sender", **hostConfig)
        receiver = self.addHost("receiver", **hostConfig)

        links = [
            (receiver, s1, 0, 1),
            (s1, s2, 2, 1),
            (s2, s3, 2, 1),
            (s3, sender, 2, 0),
        ]

        for node1, node2, port1, port2 in links:
            # Add link to topology
            self.addLink(node1, node2, port1=port1, port2=port2, **linkConfig)
