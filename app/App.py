from flask import Flask
from app.src.rutes.equity_rutes import equity

app = Flask(__name__)
app.register_blueprint(equity)

if __name__ == '__main__':
	app.run(debug=True, port=5000)
