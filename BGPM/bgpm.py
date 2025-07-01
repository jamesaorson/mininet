#!/usr/bin/env python3

import pybgpstream

"""
CS 6250 BGP Measurements Project

Notes:
- Edit this file according to the project description and the docstrings provided for each function
- Do not change the existing function names or arguments
- You may add additional functions but they must be contained entirely in this file
"""


# Task 1A: Unique Advertised Prefixes Over Time
def unique_prefixes_by_snapshot(cache_files):
    """
    Retrieve the number of unique IP prefixes from each of the input BGP data files.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A list containing the number of unique IP prefixes for each input file.
        For example: [2, 5]
    """
    # the required return type is 'list' - you are welcome to define additional data structures, if needed
    unique_prefixes_by_snapshot = []

    for fpath in cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        prefixes_seen = set()
        for elem in stream:
            prefix = elem.fields.get("prefix")
            if prefix:
                prefixes_seen.add(prefix)
        unique_prefixes_by_snapshot.append(len(prefixes_seen))
    return unique_prefixes_by_snapshot


# Task 1B: Unique Autonomous Systems Over Time
def unique_ases_by_snapshot(cache_files):
    """
    Retrieve the number of unique ASes from each of the input BGP data files.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A list containing the number of unique ASes for each input file.
        For example: [2, 5]
    """
    # the required return type is 'list' - you are welcome to define additional data structures, if needed
    unique_ases_by_snapshot = []

    for fpath in cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        ases_seen = set()
        for elem in stream:
            as_path = elem.fields.get("as-path")
            if not as_path:
                continue
            ases = as_path.split()
            ases_seen.update(ases)
        unique_ases_by_snapshot.append(len(ases_seen))

    return unique_ases_by_snapshot


# Task 1C: Top-10 Origin AS by Prefix Growth
def top_10_ases_by_prefix_growth(cache_files):
    """
    Compute the top 10 origin ASes ordered by percentage increase of advertised prefixes (smallest to largest)

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A list of the top 10 origin ASes ordered by percentage increase of advertised prefixes (smallest to largest)
        AS numbers are represented as strings.

        For example: ["777", "1", "6"]
          corresponds to AS "777" as having the smallest percentage increase (of the top ten) and AS "6" having the
          highest percentage increase (of the top ten).
    """
    # the required return type is 'list' - you are welcome to define additional data structures, if needed
    top_10_ases_by_prefix_growth = []
    as_prefixes = {}

    for ndx, fpath in enumerate(cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        as_prefixes_per_file = {}
        for elem in stream:
            as_path = elem.fields.get("as-path")
            prefix = elem.fields.get("prefix")
            if not as_path or not prefix:
                continue
            origin = as_path.split()[-1]
            if origin not in as_prefixes_per_file:
                as_prefixes_per_file[origin] = set()
            as_prefixes_per_file[origin].add(prefix)
        for _as, prefixes in as_prefixes_per_file.items():
            if _as not in as_prefixes:
                as_prefixes[_as] = []
            as_prefixes[_as].append(len(prefixes))
    percentage_growths = []
    for _as, prefixes in as_prefixes.items():
        smallest = prefixes[0]
        largest = prefixes[-1]
        percentage_growths.append((_as, (largest - smallest) / smallest))
    percentage_growths.sort(key=lambda x: x[1], reverse=False)
    top_10_ases_by_prefix_growth = [as_info[0] for as_info in percentage_growths[-10:]]
    return top_10_ases_by_prefix_growth


# Task 2: Routing Table Growth: AS-Path Length Evolution Over Time
def shortest_path_by_origin_by_snapshot(cache_files):
    """
    Compute the shortest AS path length for every origin AS from input BGP data files.

    Retrieves the shortest AS path length for every origin AS for every input file.

    Your code should return a dictionary where every key is a string representing an AS name and every value is a list
    of the shortest path lengths for that AS.

    Note: If a given AS is not present in an input file, the corresponding entry for that AS and file should be zero (0)
    Every list value in the dictionary should have the same length.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A dictionary where every key is a string representing an AS name and every value is a list, containing one entry
        per file, of the shortest path lengths for that AS
        AS numbers are represented as strings.

        Example:
        Given three cache files (also called "snapshots"), the results {"455": [4, 2, 3], "533": [4, 10, 2]}
        mean that AS 455 has a shortest path length of 4 in the first cache file, a shortest path length of 2 in the second
        cache file, and a shortest path of 3 in the third cache file. Similarly, AS 533 has shortest path lengths of 4, 10, and 2.
    """
    # the required return type is 'dict' - you are welcome to define additional data structures, if needed
    shortest_path_by_origin_by_snapshot = {}

    for ndx, fpath in enumerate(cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", fpath)

        # implement your solution here
        for elem in stream:
            as_path = elem.fields.get("as-path")
            if not as_path:
                continue
            split_as_path = as_path.split()
            origin = split_as_path[-1]
            path_length = len(set(split_as_path))
            if path_length == 1:
                continue
            if origin not in shortest_path_by_origin_by_snapshot:
                shortest_path_by_origin_by_snapshot[origin] = [0] * len(
                    cache_files,
                )
            existing_length = shortest_path_by_origin_by_snapshot[origin][ndx]
            shortest_path_by_origin_by_snapshot[origin][ndx] = (
                path_length
                if existing_length == 0
                else min(
                    existing_length,
                    path_length,
                )
            )
    return shortest_path_by_origin_by_snapshot


def _event_durations(
    elem: pybgpstream.BGPElem,
    timestamps: dict[str, dict[str, float]],
    event_durations: dict[str, dict[str, list[float]]],
    do_blackholing: bool = False,
):
    event_type = elem.type
    timestamp = elem.record.time
    peer_ip = elem.peer_address
    prefix = elem.fields.get("prefix")
    communities = elem.fields.get("communities", [])
    if not prefix or not peer_ip:
        return

    match event_type:
        case "A":
            is_rtbh_event = (
                any("666" == community.split(":")[-1] for community in communities)
                if do_blackholing
                else True
            )
            if is_rtbh_event:
                if peer_ip not in timestamps:
                    timestamps[peer_ip] = {}
                timestamps[peer_ip][prefix] = timestamp
            else:
                if peer_ip in timestamps and prefix in timestamps[peer_ip]:
                    del timestamps[peer_ip][prefix]
        case "W":
            if peer_ip not in timestamps:
                return
            if prefix not in timestamps[peer_ip]:
                return
            duration = timestamp - timestamps[peer_ip][prefix]
            if duration == 0.0:
                return
            if peer_ip not in event_durations:
                event_durations[peer_ip] = {}
            if prefix not in event_durations[peer_ip]:
                event_durations[peer_ip][prefix] = []
            event_durations[peer_ip][prefix].append(duration)
            del timestamps[peer_ip][prefix]


# Task 3: Announcement-Withdrawal Event Durations
def aw_event_durations(cache_files):
    """
    Identify Announcement and Withdrawal events and compute the duration of all explicit AW events in the input BGP data

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A dictionary where each key is a string representing the address of a peer (peerIP) and each value is a
        dictionary with keys that are strings representing a prefix and values that are the list of explicit AW event
        durations (in seconds) for that peerIP and prefix pair.

        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
    """
    # the required return type is 'dict' - you are welcome to define additional data structures, if needed
    aw_event_durations = {}
    timestamps = {}

    for ndx, fpath in enumerate(cache_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "upd-file", fpath)

        # implement your solution here
        for elem in stream:
            event_type = elem.type
            timestamp = elem.record.time
            peer_ip = elem.peer_address
            prefix = elem.fields.get("prefix")
            if not prefix or not peer_ip:
                continue
            match event_type:
                case "A":
                    if peer_ip not in timestamps:
                        timestamps[peer_ip] = {}
                    timestamps[peer_ip][prefix] = timestamp
                case "W":
                    if peer_ip not in timestamps:
                        continue
                    if prefix not in timestamps[peer_ip]:
                        continue
                    duration = timestamp - timestamps[peer_ip][prefix]
                    if duration == 0.0:
                        continue
                    if peer_ip not in aw_event_durations:
                        aw_event_durations[peer_ip] = {}
                    if prefix not in aw_event_durations[peer_ip]:
                        aw_event_durations[peer_ip][prefix] = []
                    aw_event_durations[peer_ip][prefix].append(duration)
                    del timestamps[peer_ip][prefix]
    return aw_event_durations


# Task 4: RTBH Event Durations
def rtbh_event_durations(cache_files):
    """
    Identify blackholing events and compute the duration of all RTBH events from the input BGP data

    Identify events where the prefixes are tagged with at least one Remote Triggered Blackholing (RTBH) community.

    Args:
        cache_files: A chronologically sorted list of absolute (also called "fully qualified") path names

    Returns:
        A dictionary where each key is a string representing the address of a peer (peerIP) and each value is a
        dictionary with keys that are strings representing a prefix and values that are the list of explicit RTBH event
        durations (in seconds) for that peerIP and prefix pair.

        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
    """
    # the required return type is 'dict' - you are welcome to define additional data structures, if needed
    rtbh_event_durations = {}
    timestamps = {}

    for fpath in cache_files:
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "upd-file", fpath)

        # implement your solution here
        for elem in stream:
            event_type = elem.type
            timestamp = elem.record.time
            peer_ip = elem.peer_address
            prefix = elem.fields.get("prefix")
            communities = elem.fields.get("communities", [])
            if not prefix or not peer_ip:
                continue

            match event_type:
                case "A":
                    is_rtbh_event = any(
                        "666" == community.split(":")[-1] for community in communities
                    )
                    if is_rtbh_event:
                        if peer_ip not in timestamps:
                            timestamps[peer_ip] = {}
                        timestamps[peer_ip][prefix] = timestamp
                    else:
                        if peer_ip in timestamps and prefix in timestamps[peer_ip]:
                            del timestamps[peer_ip][prefix]
                case "W":
                    if peer_ip not in timestamps:
                        continue
                    if prefix not in timestamps[peer_ip]:
                        continue
                    duration = timestamp - timestamps[peer_ip][prefix]
                    if duration == 0.0:
                        continue
                    if peer_ip not in rtbh_event_durations:
                        rtbh_event_durations[peer_ip] = {}
                    if prefix not in rtbh_event_durations[peer_ip]:
                        rtbh_event_durations[peer_ip][prefix] = []
                    rtbh_event_durations[peer_ip][prefix].append(duration)
                    del timestamps[peer_ip][prefix]
    return rtbh_event_durations
