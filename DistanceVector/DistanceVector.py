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
        def __init__(self, sender, distances):
            """Constructor. This is run once when the Message object is created."""
            self.sender = sender
            self.distances = distances

    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(
            name, topolink, outgoing_links, incoming_links
        )
        self.distances = {
            # Distance to self is always 0
            self.name: 0
        }
        for neighbor in self.outgoing_links:
            self.distances[neighbor.name] = int(neighbor.weight)

        self.MIN_DISTANCE = -99
        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data

    def new_message(self):
        return DistanceVector.Message(self.name, self.distances)

    def send_initial_messages(self):
        """This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here.

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight"""

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        for neighbor in self.neighbor_names:
            if neighbor != self.name:
                message = self.new_message()
                self.send_msg(message, neighbor)

    def process_BF(self):
        """This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent."""

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        is_updated = False
        for message in self.messages:
            # Iterate through the distance vector from the message
            for node, distance in message.distances.items():
                if node == self.name:
                    # Skip the distance to self, since it is always 0
                    continue
                # If I have not seen this neighbor before, set the distance immediately
                new_distance = self.distances[message.sender] + distance
                if node in self.distances and new_distance >= self.distances[node]:
                    continue
                if new_distance < self.MIN_DISTANCE:
                    self.distances[node] = self.MIN_DISTANCE
                else:
                    self.distances[node] = new_distance
                    is_updated = True

        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if is_updated:
            self.send_initial_messages()

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
            " ".join(
                f"({node},{distance})" for node, distance in self.distances.items()
            ),
        )
