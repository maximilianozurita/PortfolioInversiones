from flask import Flask
from app.src.resources.stocks import stocks
from app.src.resources.transactions import stransactions

app = Flask(__name__)
app.register_blueprint(stocks)
app.register_blueprint(stransactions)

if __name__ == '__main__':
	app.run(debug=True, port=5000)
