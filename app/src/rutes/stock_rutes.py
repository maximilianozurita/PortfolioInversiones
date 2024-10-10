from flask import Blueprint, request, jsonify
import src.controllers.stock_controller as stock_controller
stock = Blueprint('stock', __name__)

@stock.route('/setTransaction', methods=['POST'])
def set_new_transaction():
	data = request.json
	return stock_controller.set_new_transaction(data)

@stock.route('/stockHolding', methods=['GET'])
def stock_holding():
	return stock_controller.get_stock_holding()


@stock.route('/history', methods=['GET'])
def history():
	id = request.args.get('id')
	if id:
		response, code = stock_controller.get_history_by_id(id)
	else:
		response, code = stock_controller.get_history_list()
	return jsonify(response), code


@stock.route('/revertTransaction', methods=['GET'])
def revert_transaction(id):
	id = request.args.get("id")
	return stock_controller.revert_transaction(id)

@stock.route('/deleteHistory', methods=['GET'])
def delete_history():
	id = request.args.get("id")
	return stock_controller.delete_history(id)
