from flask import Blueprint, request, jsonify
import src.services.stock_service as stock_service
stock = Blueprint('stransactions', __name__)

@stock.route('/transactions', methods=['PUT'])
def set_new_transaction():
	data = request.json
	return stock_service.set_new_transaction(data)

@stock.route('/transactions', methods=['GET'])
def transaction():
	id = request.args.get('id')
	if id:
		response, code = stock_service.get_transaction_by_id(id)
	else:
		response, code = stock_service.get_transaction_list()
	return jsonify(response), code

# @stock.route('/transactions/<int:transaction_id>/revert', methods=['POST'])
# def revert_transaction(id):
# 	id = request.args.get("id")
# 	return stock_controller.revert_transaction(id)

@stock.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction():
	id = request.args.get("id")
	return stock_service.delete_transaction(id)