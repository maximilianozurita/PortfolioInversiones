from flask import Blueprint, request, jsonify
import src.services.stock_service as stock_service
stock = Blueprint('stocks', __name__)

@stock.route('/transactions', methods=['PUT'])
def set_new_transaction():
	data = request.json
	return stock_service.set_new_transaction(data)

@stock.route('/stocks', methods=['GET'])
def stock_holding():
	return stock_service.get_stock_holding()