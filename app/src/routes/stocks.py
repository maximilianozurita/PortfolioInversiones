from flask import Blueprint, request, jsonify
import src.services.stock_service as stock_service
from src.routes.routes_base import create_response
stock = Blueprint('stocks', __name__)

@stock.route('/transactions', methods=['PUT'])
def set_new_transaction():
	data = request.json
	r = stock_service.set_new_transaction(data)
	code = 204 if r["ok"] else 500
	return create_response(r), code

@stock.route('/stocks', methods=['GET'])
def stock_holding():
	r = stock_service.get_stock_holding()
	code = 204 if r["ok"] else 500
	return create_response(r), code