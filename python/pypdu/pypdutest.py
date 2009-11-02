import unittest
from struct import *
from pypdu import PyPdu as PyPdu

class PyPduTest(unittest.TestCase):

    def setUp(self):
        self.__pdu = PyPdu()

    def tearDown(self):
        pass

    def testConvertAcsiiToPdu(self):
        resHex = "E8329BFD4697D9EC37"
        ascii = "hellohello"
        pdu = self.__pdu.convertAsciiToPdu(ascii)
        self.assert_(pdu != None)
        print pdu
        self.assert_(pdu == resHex)

    def testConvertPduToAscii(self):
        resAscii = "hellohello"
        pdu = "E8329BFD4697D9EC37"
        ascii = self.__pdu.convertPduToAscii(pdu)
        self.assert_(ascii != None)
        print ascii
