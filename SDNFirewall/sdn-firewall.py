#!/usr/bin/python
# CS 6250 Fall 2024- SDN Firewall Project with POX
# build hackers-45

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.revent import *
from pox.lib.addresses import IPAddr, EthAddr

# You may use this space before the firewall_policy_processing function to add any extra function that you
# may need to complete your firewall implementation.  No additional functions "should" be required to complete
# this assignment.

"""Instructions:
1. Create an OpenFlow Flow Modification object
2. Create a POX Packet Matching object that will integrate the elements from a single entry in
   the firewall configuration rule file (which is passed in the policy dictionary) to match the
   different IP and TCP/UDP headers if there is anything to match (i.e., no “-“ should be passed
   to the match object, nor should None be passed to a match object if a “-“ is provided).
3. Create a POX Output Action, if needed, to specify what to do with the traffic.
"""

"""
TODO: Failed testcase from alt:
Passed 45 / 46
failed testcases:
15: h43 -> h8 with T at 231, should be True, current False
"""


class Policy:
    PRIORITY_BLOCK = 0
    PRIORITY_ALLOW = 10001

    """
    - of.OFPP_IN_PORT - This action will send the port back to the sender (i.e., the port it came
                        into the network on)
    - of.OFPP_NORMAL - Process the packet and handle via a normal L2/L3 legacy switch
                        configuration (i.e., send traffic to its destination without modification) -
                        See https://study-ccna.com/layer-3-switch/ for information on how normal
                        L2/L3 legacy switches work.
    - of.OFPP_FLOOD - This action will cause the traffic to be sent out to all ports except the
                        source (IN_PORT) and any ports that have flooding turned off. This is very
                        chatty and can be used to do network based attacks (see UDP Amplifications).
                        This should be avoided.
    - of.OFPP_ALL - output all OpenFlow ports except the source (IN_PORT). This is the same as
                    FLOOD but it includes ports that have had flood turned off.
    - of.OFPP_CONTROLLER - This action sends the packet to the switch controller. What
                            happens with the port depends on the state of the switch controller.
                            Thus it may work, but also may not work, based on the current state
                            of the switch.
    """
    # Found in libopenflow_01.py in the POX source code.
    OFPP_IN_PORT = 65528
    OFPP_NORMAL = 65530
    OFPP_FLOOD = 65531
    OFPP_ALL = 65532
    OFPP_CONTROLLER = 65533

    def __init__(self, policy_dict: dict):
        """
        - policy["mac-src"] = Source MAC Address (00:00:00:00:00:00) or “-“
        - policy["mac-dst"] = Destination MAC Address (00:00:00:00:00:00) ) or “-“
        - policy["ip-src"] = Source IP Address (10.0.1.1/32) in CIDR notation ) or “-“
        - policy["ip-dst"] = Destination IP Address (10.0.1.1/32) ) or “-“
        - policy["ipprotocol"] = IP Protocol (6 for TCP) ) or “-“
        - policy["port-src"] = Source Port for TCP/UDP (12000) ) or “-“
        - policy["port-dst"] = Destination Port for TCP/UDP (80) ) or “-“
        - policy["rulenum"] = Rule Number (1)
        - policy["comment"] = Comment (Example Rule)
        - policy["action"] = Allow or Block
        """
        self.rulenum = policy_dict["rulenum"]
        self.action = policy_dict["action"]
        self.mac_src = (
            EthAddr(policy_dict["mac-src"]) if policy_dict["mac-src"] != "-" else None
        )
        self.mac_dst = (
            EthAddr(policy_dict["mac-dst"]) if policy_dict["mac-dst"] != "-" else None
        )
        self.ip_src = policy_dict["ip-src"] if policy_dict["ip-src"] != "-" else None
        self.ip_dst = policy_dict["ip-dst"] if policy_dict["ip-dst"] != "-" else None
        self.ip_protocol = (
            int(policy_dict["ipprotocol"]) if policy_dict["ipprotocol"] != "-" else None
        )
        self.port_src = (
            int(policy_dict["port-src"]) if policy_dict["port-src"] != "-" else None
        )
        self.port_dst = (
            int(policy_dict["port-dst"]) if policy_dict["port-dst"] != "-" else None
        )
        self.comment = policy_dict["comment"]

    def _make_match(self) -> of.ofp_match:
        matchobj = of.ofp_match()
        # Set Ethernet type to IPv4
        matchobj.dl_type = pkt.ethernet.IP_TYPE

        if self.mac_src is not None:
            matchobj.dl_src = self.mac_src
        if self.mac_dst is not None:
            matchobj.dl_dst = self.mac_dst
        if self.ip_src is not None:
            matchobj.nw_src = self.ip_src
        if self.ip_dst is not None:
            matchobj.nw_dst = self.ip_dst
        if self.port_src is not None:
            matchobj.tp_src = self.port_src
        if self.port_dst is not None:
            matchobj.tp_dst = self.port_dst
        if self.ip_protocol is not None:
            matchobj.nw_proto = self.ip_protocol

        return matchobj

    def make_rule(self) -> of.ofp_flow_mod:
        rule = of.ofp_flow_mod()
        rule.priority = (
            self.PRIORITY_ALLOW
            if self.action.lower() == "allow"
            else self.PRIORITY_BLOCK
        )
        rule.match = self._make_match()
        # If blocking, we do not need to add an action
        if self.action.lower() == "block":
            return rule
        rule.actions.append(of.ofp_action_output(port=self.OFPP_CONTROLLER))
        return rule


def firewall_policy_processing(policies):
    """
    This is where you are to implement your code that will build POX/Openflow Match and Action operations to
    create a dynamic firewall meeting the requirements specified in your configure.pol file.  Do NOT hardcode
    the IP/MAC Addresses/Protocols/Ports that are specified in the project description - this code should use
    the values provided in the configure.pol to implement the firewall.

    The policies passed to this function is a list of dictionary objects that contain the data imported from the
    configure.pol file.  The policy variable in the "for policy in policies" represents a single line from the
    configure.pol file.  Each of the configuration values are then accessed using the policy['field'] command.
    The fields are:  'rulenum','action','mac-src','mac-dst','ip-src','ip-dst','ipprotocol','port-src','port-dst',
    'comment'.

    Your return from this function is a list of flow_mods that represent the different rules in your configure.pol file.

    Implementation Hints:
    The documentation for the POX controller is available at https://noxrepo.github.io/pox-doc/html .  This project
    is using the gar-experimental branch of POX in order to properly support Python 3.  To complete this project, you
    need to use the OpenFlow match and flow_modification routines (https://noxrepo.github.io/pox-doc/html/#openflow-messages
    for flow_mod and https://noxrepo.github.io/pox-doc/html/#match-structure for match.)  Also, do NOT wrap IP Addresses with
    IPAddr() unless you reformat the CIDR notation.  Look at the https://github.com/att/pox/blob/master/pox/lib/addresses.py
    for what POX is expecting as an IP Address.
    """

    policies = [Policy(policy) for policy in policies]
    rules = []
    for policy in policies:
        # Enter your code here to implement matching and block/allow rules.  See the links
        # in Implementation Hints on how to do this.
        # HINT:  Think about how to use the priority in your flow modification.

        # Please note that you need to redefine this variable below to create a valid POX Flow Modification Object
        rule = policy.make_rule()

        # End Code Here
        print("Added Rule ", policy.rulenum, ": ", policy.comment)
        # print(rule)   #Uncomment this to debug your "rule"
        rules.append(rule)

    return rules
