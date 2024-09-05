import unittest
from tests.unitTests.FactoryTest.TestFactoryStock import testFactoryStock
from tests.unitTests.Helpers.TestMsgHandler import testMsgHandler
from tests.unitTests.Model.TestStock import testStock
from tests.unitTests.Model.TestTicket import testTicket
from tests.unitTests.Model.TestConector import testConector

modules = [
	testMsgHandler,
	testFactoryStock,
	testStock,
	testTicket,
	testConector
]

def suite():
	loader = unittest.TestLoader()
	suite = unittest.TestSuite()
	for testCase in modules:
		suite.addTests(loader.loadTestsFromTestCase(testCase))
		test_case_names = loader.getTestCaseNames(testCase)
		print("Test cases in " + testCase.__name__ + ": ", test_case_names)
	return suite

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	runner.run(suite())
