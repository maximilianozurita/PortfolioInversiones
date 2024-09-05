from src.models.conector import conectorBase

class Ticket:
	_tabla = "tickets"
	def __init__(self, ticket, loadAll = 0):
		self.ticket = ticket
		if loadAll:
			self.name = loadAll["name"]
			self.ratio = loadAll["ratio"]
			self.date = loadAll["date"]
		else:
			self._cargar_datos()

	def _cargar_datos(self):
		conector = conectorBase()
		query = "SELECT * from " + self._tabla + " WHERE ticket = %s"
		result = conector.selectOne(query, [self.ticket])
		for attr in result:
			setattr(self, attr, result[attr])

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
		return Ticket(attrsExpected["ticket"])