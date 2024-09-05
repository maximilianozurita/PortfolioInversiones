# import tests.Factory.Register as FactoryRegister
from tests.Factory.FactoryRegister import FactoryRegister
import unittest

class testBase(unittest.TestCase):
	def setUp(self):
		self.factory = FactoryRegister()
		print(f"Running test: {self.id().split('.')[-1]}")

	def tearDown(self):
		print(f"Ending test: {self.id().split('.')[-1]}")
		objtsToDelete = self.factory.createdObjects
		for obj in objtsToDelete:
			obj.delete()

	def assertAttrsEquals(self, obj1, obj2):
		attr1 = obj1.__dict__
		attr2 = obj2.__dict__
		self.assertEqual(attr1, attr2)
