from src.helpers.msgsHandler import msgsHandler
from tests.unitTests.Base import testBase, unittest

class testMsgHandler(testBase):
	def testMsgWithArgs(self):
		msgs = msgsHandler()
		key = "peso"
		msgParsed = msgs.getMessage("test_msj1_params", [key])
		self.assertIsInstance(msgParsed, str)
		self.assertIn(key, msgParsed)

	def testMsgWithoutArgs(self):
		msgs = msgsHandler()
		msgParsed = msgs.getMessage("test_msj_sin_params")
		self.assertIsInstance(msgParsed, str)

	def testMsgWithMultipleArgs(self):
		msgs = msgsHandler()
		key1 = "prueba"
		key2 = "prueba2"
		msgParsed = msgs.getMessage("test_msj2_params", [key1, key2])
		self.assertIsInstance(msgParsed, str)
		self.assertIn(key1, msgParsed)
		self.assertIn(key2, msgParsed)

	def testErrorMsgWithoutArgs(self):
		msgs = msgsHandler()
		msgParsed = msgs.getMessage("test_msj1_params")
		self.assertIsInstance(msgParsed, str)
		self.assertEqual(msgParsed, "")

	def testErrorMsgWithExtraParams(self):
		msgs = msgsHandler()
		msgParsed = msgs.getMessage("test_msj1_params", ["prueba", "prueba2"])
		self.assertIsInstance(msgParsed, str)
		self.assertEqual(msgParsed, "")

	def testErrorMsgWithLessParams(self):
		msgs = msgsHandler()
		msgParsed = msgs.getMessage("test_msj2_params", ["prueba"])
		self.assertIsInstance(msgParsed, str)
		self.assertEqual(msgParsed, "")

	def testErrorMsgWithParamNoArray(self):
		msgs = msgsHandler()
		msgParsed = msgs.getMessage("test_msj2_params", "prueba")
		self.assertIsInstance(msgParsed, str)
		self.assertEqual(msgParsed, "")

	def testPrintMultipleErrors(self):
		#Ver posibilidad de en lugar de printear, de devolver array de msj
		errors = {
			"test_msj_sin_params" : [[]],
			"test_msj1_params": [["prueba"]],
			"test_msj2_params": [["prueba", "prueba2"], ["prueb3", "prueba4"]]
		}
		msgsHandler.printErrors(errors)

if __name__ == '__main__':
	unittest.main()