from flask import Blueprint, request

from lib.chain import Chain
from lib.network import broadcast_quant
from lib.transactions import load_transactions, save_transactions

def construct_mining_blueprint(live_nodes, port):

    mining_blueprint = Blueprint('mining', __name__)

    @mining_blueprint.route('/leap', methods=['GET'])
    # Route to trigger ad-hoc mining
    # TODO: make mining configurable and automathic so POS and DPOS can be implemented
    def generate_block():
        QBC = Chain()
        if request.method == 'GET':
            # Below is super simple, the idea is to have decision model on number of transactions and 
            # also which transactions go in
            print "Starting leap"
            new_quant_data = load_transactions()
            new_quant = QBC.create_quant(new_quant_data)
            print new_quant
            broadcast_quant(live_nodes, new_quant)
            save_transactions([])   
            print "Quantum leap"	
            return "block creation successful\n"
    
    return mining_blueprint