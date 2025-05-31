# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):
    class Message:
        def __init__(self, source, vector):
            self.source = source
            self.vector = vector

    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(
            name, topolink, outgoing_links, incoming_links
        )
        self.vector = {self.name: 0}
        self.MIN_DISTANCE = -99

    def send_initial_messages(self):
        self.send_to_incoming_links()

    def send_to_incoming_links(self):
        for link in self.incoming_links:
            message = DistanceVector.Message(
                self.name,
                self.vector.copy(),
            )
            self.send_msg(message, link.name)

    def get_weight(self, name):
        _, weight = self.get_outgoing_neighbor_weight(name)
        return int(weight)

    def process_BF(self):
        is_updated = False
        for msg in self.messages:
            for node in msg.vector.keys():
                if node not in self.vector and node != self.name:
                    if self.is_outgoing_neighbor(node):
                        nodeWeight = int(self.get_weight(node))
                    else:
                        nodeWeight = int(self.get_weight(msg.source)) + int(
                            msg.vector[node]
                        )
                    self.vector[node] = nodeWeight
                    is_updated = True
                elif node in self.vector and node != self.name:
                    sourceNode_to_vector = int(self.get_weight(msg.source))
                    vector_to_sourceNode = int(msg.vector[node])
                    updated_distance = sourceNode_to_vector + vector_to_sourceNode

                    if (
                        sourceNode_to_vector <= self.MIN_DISTANCE
                        or vector_to_sourceNode <= self.MIN_DISTANCE
                        and self.vector[node] != self.MIN_DISTANCE
                    ):
                        self.vector[node] = self.MIN_DISTANCE
                        is_updated = True
                    else:
                        if (
                            updated_distance < self.vector[node]
                            and updated_distance > self.MIN_DISTANCE
                        ):
                            self.vector[node] = updated_distance
                            is_updated = True
                        elif (
                            updated_distance <= self.MIN_DISTANCE
                            and self.vector[node] != self.MIN_DISTANCE
                        ):
                            self.vector[node] = self.MIN_DISTANCE
                            is_updated = True
        self.messages = []
        if is_updated:
            self.send_to_incoming_links()

    def is_outgoing_neighbor(self, name):
        return any(link.name == name for link in self.outgoing_links)

    def log_distances(self):
        """This function is called immedately after process_BF each round.  It
        prints distances to the console and the log file in the following format (no whitespace either end):

        A:(A,0) (B,1) (C,-2)

        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0"""

        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.
        add_entry(
            self.name,
            " ".join(f"({name},{distance})" for name, distance in self.vector.items()),
        )
