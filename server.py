import json

import sys

from flask import Flask, request

from flask_socketio import SocketIO, emit



from modules.creation import bang, create_next_quant
from modules.quant import Quant



node = Flask(__name__)
socketio = SocketIO(node)
"""
Basic blockchain sever with ability to 

* register self on the system
* accept data to insert
* register new node form the system
* send local chain stats
* send local chain

"""
local_qbc = [bang()]
last_quant = local_qbc[0]
live_nodes = []

@node.route('/quant', methods=['POST'])
def add_block():
  if request.method == 'POST':
		new_quant_data = request.get_json()
		new_quant = create_next_quant(last_quant, new_quant_data)
		local_qbc.append(new_quant)
		print "New block added"	
		print "{}".format(new_quant)
		return "Submission successful\n"

@node.route('/chain', methods=['GET'])
def serve_qbc():
	if request.method == 'GET':
		exported_qbc = [{
				"index": str(quant.index),
				"timestamp": str(quant.timestamp),
				"data": str(quant.data),
				"hash": quant.hash
				} for quant in local_qbc]
				
		exported_qbc = json.dumps(exported_qbc)
		return exported_qbc

@node.route('/discover', methods=['POST', 'GET'])
def register_node():
	if request.method == 'GET':
		return json.dumps(live_nodes)
	if request.method == 'POST':
		live_nodes.append(request.get_json()['host'])
		return "SUCCESS!!!"



@socketio.on('connect', namespace='/ptp')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/ptp')
def test_disconnect():
    print('Client disconnected')



port = int(sys.argv[1]) if (len(sys.argv) >= 2) else 5000

node.run(port=port, debug=True)