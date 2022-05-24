import flask
import blockchain
import jsonify
from flask import jsonify, request
from uuid import uuid4

app = flask.Flask(__name__)
node_address = str(uuid4()).replace('-', '')
blockchain = blockchain.Blockchain()


@app.route('/mine-block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(sender=node_address, receiver='John', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "block": block
    }
    return jsonify(response), 200


@app.route('/get-chain', methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "len": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/check-chain', methods=["GET"])
def check_chain():
    response = {
        "valid": blockchain.is_chain_valid(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/add_transaction', methods=["POST"])
def add_transaction():
    json = request.get_json()
    transaction_keys = ["sender", "receiver", "amount"]
    if not all(key in json for key in transaction_keys):
        return "Some elements of the transaction is missing", 400
    index = blockchain.add_transactions(json["sender"], json["receiver"], json["amount"])
    response = {
        "message": f"This transaction will be added to block{index}"
    }
    return jsonify(response), 200


@app.route('/connect-node', methods=["POST"])
def connect_node():
    json = request.get_json()
    nodes = json.get("nodes")
    if nodes is None:
        return "No Node", 400

    for node in nodes:
        blockchain.add_nodes(node)

    response = {
        "Nodes": list(blockchain.nodes)
    }
    return jsonify(response), 200


@app.route('/replace-chain', methods=["GET"])
def replace_chain():
    is_valid_replace = blockchain.replace_chain()
    if is_valid_replace:
        response = {
            "Message": "Good"
        }
    else:
        response = {
            "Message": "Bad"
        }

    return jsonify(response), 200


app.run(host='localhost', port=5001)
