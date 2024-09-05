from flask import request
import helpers.stockHelper as stockHelper
import models.stockModel as stockModel
import models.historyModel as historyModel

def set_new_transaction(data):
    stock_holding = stockModel.get_hold_stock_by_ticket(data['ticket'])
    return update_holding_stock(data, stock_holding)

def revert_transaction(id):
    data = historyModel.get_history(id)
    update_holding_stock(data, stockModel.get_hold_stock_by_ticket(data['ticket']))
    historyModel.delete_history(id)
    return {'message': 'eliminado'}

def delete_history(id):
    historyModel.delete_history(id)
    return {'message': 'eliminado'}

def get_history_by_id(id):
    return historyModel.get_history(id)

def get_history_list():
    return historyModel.get_all_history()

def get_stock_holding():
    return stockModel.get_stock_holding()

def update_holding_stock(data, stock_holding):
    if stock_holding['quantity'] + data['quantity'] < 0:
        print('No hay suficientes acciones para eliminar')
        return {'error': 'no hay suficientes acciones para eliminar'}
    else:
        msg = ''
        if stock_holding['quantity'] + data['quantity'] == 0:
            stockModel.delete_stock_holding(stock_holding['ticket'])
            msg = {'message': 'eliminado'}
        else:
            new_stock_holding = stockHelper.get_new_stock_holding_data(stock_holding, data)
            stockModel.set_stock_holding(new_stock_holding)
            msg = {'message': 'eliminado'}
        historyModel.set_transaction(data)
        return msg
