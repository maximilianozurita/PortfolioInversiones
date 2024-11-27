from flask import Blueprint, request
from src.routes.routes_base import create_response
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
		r = stock_service.get_transaction_by_id(id)
	else:
		r = stock_service.get_transaction_list()
	code = 200 if r["ok"] else 404
	return create_response(r), code


@stock.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
def delete_transaction():
	id = request.args.get("id")
	r = stock_service.delete_transaction(id)
	code = 204 if r["ok"] else 500
	return create_response(r), code

# @stock.route('/transactions/<int:transaction_id>/revert', methods=['POST'])
# def revert_transaction(id):
# 	id = request.args.get("id")
# 	return stock_controller.revert_transaction(id)