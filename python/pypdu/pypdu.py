#from struct import *

class PyPdu(object):

    def convertAsciiToPdu(self, ascii):
        lastByte = None
        index = 1
        pdu = []
        for byte in ascii:
            byte = ord(byte)
            if(index > 7):
                index = 1
                lastByte = byte
                continue
            if(lastByte == None):
                lastByte = byte
                continue
            lastByte = lastByte | (byte << (8 - index))
            byte = byte >> index
            pdu.append(lastByte & 0xff)
            index += 1
            lastByte = byte
        pdu.append(lastByte & 0xff)
        return pdu

