from flask import Blueprint, request, jsonify
import controllers.equityController as equityController
equity = Blueprint('equity', __name__)

@equity.route('/setTransaction', methods=['POST'])
def set_new_transaction():
    data = request.json
    return jsonify(equityController.set_new_transaction(data))

@equity.route('/stockHolding', methods=['GET'])
def stock_holding():
    return jsonify(equityController.get_stock_holding())

@equity.route('/history', methods=['GET'])
def history():
    id = request.args.get('id')
    if id:
        return jsonify(equityController.get_history_by_id(id))
    else:
        return jsonify(equityController.get_history_list())

@equity.route('/revertTransaction', methods=['GET'])
def revert_transaction(id):
    id = request.args.get("id")
    return jsonify(equityController.revert_transaction(id))

@equity.route('/deleteHistory', methods=['GET'])
def delete_history():
    id = request.args.get("id")
    return jsonify(equityController.delete_history(id))
