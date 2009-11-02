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
        result = "".join(["%02X" % el for el in pdu])
        return result

    def convertPduToAscii(self, pdu):
        bytes = []
        runvar = len(pdu)
        i=0
        while i < runvar:
            tmp = pdu[i:i+2]
            hex = int(tmp, 16)
            bytes.append(hex)
            i += 2

        ascii = []
        index = 0
        lastByte = None
        for byte in bytes:
            if(index == 7):
                index = 0
                tmp = (lastByte >> 1) & 0x7f
                ascii.append(tmp)
                lastByte = None

            if(lastByte == None):
                tmp = byte & 0x07f
                ascii.append(tmp)
                index += 1
                lastByte = byte
                continue

            tmp = (lastByte >> (8 - index)) | ((byte << index) & 0x7f)
            ascii.append(tmp)
            lastByte = byte
            index += 1

        result = "".join(["%c" % el for el in ascii])
        return result
