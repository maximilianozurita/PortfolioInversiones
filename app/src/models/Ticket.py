from src.models.conector import conectorBase

class Ticket:
	_tabla = "tickets"
	def __new__(cls, ticket, data = None):
		if ticket is not None:
			if not data:
				data = Ticket.loadData(ticket)
			if data:
				instance = super(Ticket, cls).__new__(cls)
				instance.ticket = data["ticket"]
				instance.name = data["name"]
				instance.ratio = data["ratio"]
				instance.date = data["date"]
				return instance
		return None

	def __repr__(self):
			attrs = ', '.join(f'{attr}={getattr(self, attr)}' for attr in vars(self))
			return self.__class__.__name__ + f'({attrs})'

	def findAll():
		conector = conectorBase()
		tickets = []
		query = "SELECT * from " + Ticket._tabla
		filas = conector.select(query)
		for fila in filas:
			tickets.append(Ticket(fila["ticket"], fila))
		return tickets

	def findOne():
		conector = conectorBase()
		query = "SELECT * from " + Ticket._tabla + " limit 1"
		attrsExpected = conector.selectOne(query)
		if attrsExpected:
			return Ticket(attrsExpected["ticket"])
		return None

	def loadData(ticket):
		conector = conectorBase()
		query = "SELECT * from " + Ticket._tabla + " WHERE ticket = %s"
		return conector.selectOne(query, [ticket])
