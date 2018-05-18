import json

from flask import Flask

from lib.chain import Chain
from lib.network import Network
from lib.qbc_utils import QbcUtils

from modules.transactions.controllers import transactions_blueprint
from modules.mining.controllers import mining_blueprint
from modules.network.controllers import network_blueprint
from modules.chain.controllers import chain_blueprint

node = Flask(__name__)

QBC = Chain()
QBCN = Network()
QBCU = QbcUtils()
port = QBCU.get_port()

# Registering all the modules
node.register_blueprint(transactions_blueprint)

node.register_blueprint(mining_blueprint)

node.register_blueprint(network_blueprint)

node.register_blueprint(chain_blueprint)


# Discover full network and register on each of the nodes
network = QBCN.discover_network()
live_nodes=network["registered_nodes"]

if not QBCU.is_genesis_node():
	QBCN.save_nodes(live_nodes)

	# If this is not first (genesis) node (meaning that at start there is noone else to look at on start),
	# take look at network stats to see if there is longer chain. If there is one - get it.
	if json.loads(QBC.get_chain_stats())["length"] < network["longest_chain_length"]:
		QBC.get_remote_node_chain(network["longest_chain_node"])


node.run(host='0.0.0.0', port=port, debug=True)