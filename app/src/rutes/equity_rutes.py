from flask import Blueprint, request, jsonify
import app.src.controllers.equity_controller as equity_controller
equity = Blueprint('equity', __name__)

@equity.route('/setTransaction', methods=['POST'])
def set_new_transaction():
    data = request.json
    return jsonify(equity_controller.set_new_transaction(data))

@equity.route('/stockHolding', methods=['GET'])
def stock_holding():
    return jsonify(equity_controller.get_stock_holding())

@equity.route('/history', methods=['GET'])
def history():
    id = request.args.get('id')
    if id:
        return jsonify(equity_controller.get_history_by_id(id))
    else:
        return jsonify(equity_controller.get_history_list())

@equity.route('/revertTransaction', methods=['GET'])
def revert_transaction(id):
    id = request.args.get("id")
    return jsonify(equity_controller.revert_transaction(id))

@equity.route('/deleteHistory', methods=['GET'])
def delete_history():
    id = request.args.get("id")
    return jsonify(equity_controller.delete_history(id))
