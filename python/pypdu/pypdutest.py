import unittest
from struct import *
from pypdu import PyPdu as PyPdu

class PyPduTest(unittest.TestCase):

    def setUp(self):
        self.__pdu = PyPdu()

    def tearDown(self):
        pass

    def testConvertAcsiiToPdu(self):
        resHex = [0xE8, 0x32, 0x9B, 0xFD, 0x46, 0x97, 0xD9, 0xEC, 0x37]
        ascii = "hellohello"
        pdu = self.__pdu.convertAsciiToPdu(ascii)
        self.assert_(pdu != None)
        self.assert_(pdu == resHex)
        
