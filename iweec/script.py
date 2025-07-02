import json
import pybgpstream

ASN = "30844"
BLACKHOLE_COMMUNITY = "666"

stream = pybgpstream.BGPStream(
    project="routeviews-stream",
    filter=f"origin {ASN}",
)

blackholed_prefixes = {}
withdrawn_prefixes = {}

for elem in stream:
    event_type = elem.type
    timestamp = elem.record.time
    peer_ip = elem.peer_address
    prefix = elem.fields.get("prefix")
    as_path = elem.fields.get("as-path", "")
    communities = elem.fields.get("communities", [])
    if not prefix or not peer_ip:
        continue

    split_path = as_path.split()
    match event_type:
        case "A":
            if ASN in split_path:
                if any(
                    BLACKHOLE_COMMUNITY in str(community) for community in communities
                ):
                    print(f"Possible blackhole detected for {prefix}")
                    if peer_ip not in blackholed_prefixes:
                        blackholed_prefixes[peer_ip] = {}
                    if prefix not in blackholed_prefixes[peer_ip]:
                        blackholed_prefixes[peer_ip][prefix] = []
                    blackholed_prefixes[peer_ip][prefix].append(
                        {
                            "timestamp": timestamp,
                            "as_path": split_path,
                            "communities": communities,
                        }
                    )
        case "W":
            print(f"Withdrew: {prefix} from {peer_ip} at {timestamp}")
            if peer_ip not in withdrawn_prefixes:
                withdrawn_prefixes[peer_ip] = {}
            if prefix not in withdrawn_prefixes[peer_ip]:
                withdrawn_prefixes[peer_ip][prefix] = set()
            withdrawn_prefixes[peer_ip][prefix].add(timestamp)

with open("blackholed_prefixes.json", "w") as f:
    json.dump(blackholed_prefixes, f, indent=4, sort_keys=True)
with open("withdrawn_prefixes.json", "w") as f:
    json.dump(withdrawn_prefixes, f, indent=4, sort_keys=True)
