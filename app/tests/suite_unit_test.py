import unittest
from tests.unit_tests.factory_test.test_factory_stock import TestFactoryStock
from tests.unit_tests.factory_test.test_factory_history import TestFactoryHistory
from tests.unit_tests.helpers.test_msg_handler import TestMsgHandler
from tests.unit_tests.model.test_stock import TestStock
from tests.unit_tests.model.test_ticket import TestTicket
from tests.unit_tests.model.test_conector import TestConector
from tests.unit_tests.model.test_history import TestHistory


modules = [
	TestMsgHandler,
	TestFactoryStock,
	TestStock,
	TestTicket,
	TestConector,
	TestHistory,
	TestFactoryHistory
]

def suite():
	loader = unittest.TestLoader()
	suite = unittest.TestSuite()
	for test_case in modules:
		suite.addTests(loader.loadTestsFromTestCase(test_case))
		test_case_names = loader.getTestCaseNames(test_case)
		print("Test cases in " + test_case.__name__ + ": ", test_case_names)
	return suite

if __name__ == "__main__":
	runner = unittest.TextTestRunner()
	runner.run(suite())
