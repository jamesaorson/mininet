import json
import pybgpstream

stream = pybgpstream.BGPStream(
    project="routeviews-stream",
    filter="origin 30844",
)

withdrawn_prefixes = {}

for elem in stream:
    event_type = elem.type
    timestamp = elem.record.time
    peer_ip = elem.peer_address
    prefix = elem.fields.get("prefix")
    communities = elem.fields.get("communities", [])
    if not prefix or not peer_ip:
        continue

    if event_type == "W":
        print(f"Withdrew: {prefix} from {peer_ip} at {timestamp}")
        if peer_ip not in withdrawn_prefixes:
            withdrawn_prefixes[peer_ip] = {}
        if prefix not in withdrawn_prefixes[peer_ip]:
            withdrawn_prefixes[peer_ip][prefix] = set()
        withdrawn_prefixes[peer_ip][prefix].add(timestamp)

with open("withdrawn_prefixes.json", "w") as f:
    json.dump(withdrawn_prefixes, f, indent=4, sort_keys=True)
