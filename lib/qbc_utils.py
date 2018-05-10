import json, socket, sys

system_config = json.load(open('./config/system_preferences.json'))

def get_current_ip():
    return socket.gethostbyname(socket.gethostname())

def get_port():
    return int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

def parse_localhost(new_node):
    """
        for testing purposes, for node to communicate inside same machine, 
        we need to parse all the IP addresses and replace current machine ones with localhost
    """
    current_node_ip = get_current_ip()
    if current_node_ip not in new_node:
        node_addr = new_node
    else:
        node_addr = new_node.replace(current_node_ip, "localhost")
    return node_addr

def get_hostname(ip, port):
    # TODO: handle different protocols
    return "http://{}:{}".format(ip, port)

def is_genesis_node():
    """
        Shows if current node belongs to list of initial nodes 
        (it usually mean that those will stay longest time - i.e. forever)
    """
    genesis_nodes = system_config["genesis_nodes"]
    this_node = get_hostname(get_current_ip(), get_port())
    return this_node in genesis_nodes or parse_localhost(this_node) in genesis_nodes