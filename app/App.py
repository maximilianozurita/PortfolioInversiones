from flask import Flask
from app.src.rutes.stock_rutes import stock

app = Flask(__name__)
app.register_blueprint(stock)

if __name__ == '__main__':
	app.run(debug=True, port=5000)
