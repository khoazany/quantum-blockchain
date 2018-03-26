import datetime as date
import json, pickle, os

from modules.quant import Quant

class Chain:
    """
    QBC structure implementation
    """
    def __init__(self):
        # If there is locally storred chain it should be read and used on init 
        # (instead of basic initiation of genesis block)
        if(os.path.exists(os.path.join(os.getcwd(),'storage', 'q.bc'))):
            self.qbc = Chain.__read_chain_from_disc()
        else:
            self.qbc = [Chain.__bang()]
        self.current_quant = self.qbc[0]
        Chain.__read_chain_from_disc()

    @classmethod
    def __bang(self):
        """Bang starts new blockchain creating what is known as 'genesis block'"""
        return Quant(0, date.datetime.now(), "Small Bang", "0", "1")
    @classmethod
    def __create_next_quant(self, last_quant, data):
        """
            Creates next block in Quantum Blockchain, known as Quant
        """
        this_index = last_quant.index + 1
        this_timestamp = date.datetime.now()
        this_data = data
        last_hash = last_quant.hash
        last_proof = last_quant.proof
        return Quant(this_index, this_timestamp, this_data, last_hash, last_proof)
    @classmethod
    def __read_chain_from_disc(self):
        with open(os.path.join(os.getcwd(),'storage', 'q.bc'), 'rb') as qbc_file:
            return pickle.load(qbc_file)


    
    def create_quant(self, data):
        """
            Public method to add new quatn to QBC
        """
        self.qbc.append(Chain.__create_next_quant(self.current_quant, data))
        self.current_quant = self.qbc[len(self.qbc) - 1]
        Chain.write_qbc_to_disc(self)

    def get_chain(self):
        return self.qbc

    def get_json_chain(self):
        """
            Getting json serialized QBC
        """
        return json.dumps([{
                    "index": str(quant.index),
                    "timestamp": str(quant.timestamp),
                    "data": str(quant.data),
                    "hash": quant.hash,
                    "proof": str(quant.proof)
                    } for quant in self.qbc])
    def write_qbc_to_disc(self):
        """
            Storing QBC on disc serualized using pickle
            TODO: introduce encryption
        """
        with open(os.path.join(os.getcwd(),'storage', 'q.bc'), 'wb') as fp:
            pickle.dump(self.qbc, fp)