import socket, json, requests

from modules.qbc_utils import parse_localhost
# registering on the network, currently no channel to broadcast, so we can use ping to everyone in genesis nodes list
# TODO: implement timeout for request and fallback... Probably hardcoded genesis node should be fallback and some (maybe serverless?) discovery mechanism should be created
# TODO: review ip fetching, must be less hacky way

def register_and_discover(node_addr, this_node):
    discover_payload = {'host': this_node}
    register_request = requests.post("{}/discover".format(node_addr), json=discover_payload)
    print("register and discover - {}".format(register_request.text))
    return register_request


def discover_network(genesis_node, live_nodes=[], port=5000):
    """
        Network discovery is done in two stages:
        1 - ping genesys node (aka tracker) to register and get it's full list of nodes
        2 - register on all of the nodes
        TODO: implement cross check and re register of nodes.
    """
    registered_nodes = live_nodes
    new_nodes = []
    if not genesis_node:
        node_ip = socket.gethostbyname(socket.gethostname())
        this_node = "http://{}:{}".format(node_ip, port)
        for qbc_node in registered_nodes:
            node_addr = parse_localhost(qbc_node)
            hosts_from_node = json.loads(register_and_discover(node_addr, this_node).text)["live_nodes"]

            new_nodes += [x for x in hosts_from_node if (x != this_node and x not in registered_nodes)]

            print("new nodes - {}".format(json.dumps(new_nodes)))

            registered_nodes = registered_nodes + new_nodes
            if(len(new_nodes) > 0):
                print("registered nodes - {}".format(json.dumps(registered_nodes)))
                for new_node in new_nodes:
                    new_node_addr = parse_localhost(new_node)
                    register_and_discover(new_node_addr, this_node)
            else:
                print("I guess this is second node on the network...")
    return registered_nodes