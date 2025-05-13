"""
/*
 * Copyright © 2022 Georgia Institute of Technology (Georgia Tech). All Rights Reserved.
 * Template code for CS 6250 Computer Networks
 * Instructors: Maria Konte
 * Head TAs: Johann Lau and Ken Westdorp
 *
 * Georgia Tech asserts copyright ownership of this template and all derivative
 * works, including solutions to the projects assigned in this course. Students
 * and other users of this template code are advised not to share it with others
 * or to make it available on publicly viewable websites including repositories
 * such as GitHub and GitLab. This copyright statement should not be removed
 * or edited. Removing it will be considered an academic integrity issue.
 *
 * We do grant permission to share solutions privately with non-students such
 * as potential employers as long as this header remains in full. However,
 * sharing with other current or future students or using a medium to share
 * where the code is widely available on the internet is prohibited and
 * subject to being investigated as a GT honor code violation.
 * Please respect the intellectual ownership of the course materials
 * (including exam keys, project requirements, etc.) and do not distribute them
 * to anyone not enrolled in the class. Use of any previous semester course
 * materials, such as tests, quizzes, homework, projects, videos, and any other
 * coursework, is prohibited in this course.
 */
"""

# Spanning Tree Protocol project for GA Tech OMSCS CS-6250: Computer Networks
#
# Copyright 2023 Vincent Hu
#           Based on prior work by Sean Donovan, Jared Scott, James Lohse, and Michael Brown

from Message import Message
from StpSwitch import StpSwitch


class Switch(StpSwitch):
    """
    This class defines a Switch (node/bridge) that can send and receive messages
    to converge on a final, loop-free spanning tree. This class
    is a child class of the StpSwitch class. To remain within the spirit of
    the project, the only inherited members or functions a student is permitted
    to use are:

    switchID: int
        the ID number of this switch object)
    links: list
        the list of switch IDs connected to this switch object)
    send_message(msg: Message)
        Sends a Message object to another switch)

    Students should use the send_message function to implement the algorithm.
    Do NOT use the self.topology.send_message function. A non-distributed (centralized)
    algorithm will not receive credit. Do NOT use global variables.

    Student code should NOT access the following members, otherwise they may violate
    the spirit of the project:

    topolink: Topology
        a link to the greater Topology structure used for message passing
    self.topology: Topology
        a link to the greater Topology structure used for message passing
    """

    def __init__(self, idNum: int, topolink: object, neighbors: list):
        """
        Invokes the super class constructor (StpSwitch), which makes the following
        members available to this object:

        idNum: int
            the ID number of this switch object
        neighbors: list
            the list of switch IDs connected to this switch object
        """
        super(Switch, self).__init__(idNum, topolink, neighbors)
        # TODO: Define class members to keep track of which links are part of the spanning tree
        self.root: int = idNum
        self.distance: int = 0
        self.closest_neighbor: int = None
        self.active_links: set[int] = set()

    def process_message(self, message: Message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        
        # INSTRUCTIONS FROM THE CLASS LECTURE:
        # a) The root of the configuration has a smaller ID, or if
        # In addition, a node stops sending configuration messages over
        # a link (port) when the node receives a configuration message
        # that indicates that it is not the root, e.g., when it receives
        # a configuration message from a neighbor that is
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1
            self.swap_closest_neighbor(message)
        # b) The roots have equal IDs, but
        elif message.root == self.root:
            # c) Both roots IDs are the same and the distances are the same, then
            # the node breaks the tie by selecting the configuration
            # of the sending node that has the smallest ID.
            # a) either closer to the root, or
            if message.distance + 1 < self.distance:
                self.distance = message.distance + 1
                self.swap_closest_neighbor(message)
            # b) has the same distance from the root, but it has a smaller ID.
            elif message.distance + 1 == self.distance:
                if message.origin < self.closest_neighbor:
                    self.swap_closest_neighbor(message)
            # FROM THE PROJECT PDF:
            # If the message has a larger distance from the root, we need to check
            # if we are the closest neighbor. If so, we add the link, else we need
            # to remove the link
            elif message.distance + 1 > self.distance:
                if message.pathThrough:
                    self.active_links.add(message.origin)
                    self.send_to_neighbors(message.ttl)
                else:
                    self.active_links.discard(message.origin)

    def swap_closest_neighbor(self, message: Message):
        self.closest_neighbor = message.origin
        self.active_links = {self.closest_neighbor}
        self.send_to_neighbors(message.ttl)

    def send_to_neighbors(self, ttl: int):
        for neighbor in self.links:
            msg = Message(self.root,
                          self.distance,
                          self.switchID,
                          neighbor,
                          neighbor == self.closest_neighbor,
                          ttl - 1)
            self.send_message(msg)

    def generate_logstring(self):
        """
        Logs this Switch's list of Active Links in a SORTED order

        returns a String of format:
            SwitchID - ActiveLink1, SwitchID - ActiveLink2, etc.
        """
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked
        #      only after the simulation is complete.  Output the links included in the
        #      spanning tree by INCREASING destination switch ID on a single line.
        #
        #      Print links as '(source switch id) - (destination switch id)', separating links
        #      with a comma - ','.
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #
        #      A full example of a valid output file is included (Logs/) in the project skeleton.
        return ", ".join(
            f"{self.switchID} - {link}" for link in sorted(self.active_links)
        )
