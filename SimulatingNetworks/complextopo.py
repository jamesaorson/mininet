from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom


# Topology to be instantiated in Mininet
class ComplexTopo(Topo):
    """Mininet Complex Topology"""

    def __init__(self, cpu=0.1, max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        # TODO: Create your Mininet Topology here!
        self.host_config = {"cpu": cpu}
        ethernet_config = {
            "bw": 25,
            "delay": "2ms",
            "loss": 0,
            "max_queue_size": max_queue_size,
        }
        wifi_config = {
            "bw": 10,
            "delay": "6ms",
            "loss": 0.03,
            "max_queue_size": max_queue_size,
        }
        three_g_config = {
            "bw": 3,
            "delay": "10ms",
            "loss": 0.08,
            "max_queue_size": max_queue_size,
        }

        s1 = self.make_switch("s1")
        s2 = self.make_switch("s2")
        s3 = self.make_switch("s3")
        s4 = self.make_switch("s4")

        h1 = self.make_host("h1")
        h2 = self.make_host("h2")
        h3 = self.make_host("h3")

        for link in [
            (h1, s1, None, None, ethernet_config),
            (s1, s2, None, None, ethernet_config),
            (s2, s3, None, None, ethernet_config),
            (s2, s4, None, None, ethernet_config),
            (s3, h2, None, None, wifi_config),
            (s4, h3, None, None, three_g_config),
        ]:
            self.make_link(*link)

    def make_host(self, name: str):
        return self.addHost(name, **self.host_confi)

    def make_switch(self, name: str):
        return self.addSwitch(name)

    def make_link(self, node1, node2, port1: int, port2: int, link_config: dict):
        return self.addLink(node1, node2, port1=port1, port2=port2, **link_config)
