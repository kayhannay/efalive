#from struct import *
import getopt
import sys

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

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hap", ["help"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    pduFormat = False
    for o, a in opts:
        if o == "-a":
            pduFormat = False
        elif o == "-p":
            pduFormat = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if(args == None or len(args) == 0):
        print "Missing parameter"
        usage()
        sys.exit(2)
    pdu = PyPdu()
    for arg in args:
        result = None
        if pduFormat:
            result = pdu.convertPduToAscii(arg)
        else:
            result = pdu.convertAsciiToPdu(arg)
        if(len(arg) > 40):
            print "%s:" % arg
            print "  %s" % result
        else:
            print "%s : %s" % (arg, result)
    

def usage():
    print ""
    print "PyPdu version 0.5"
    print "This tool can be used to convert 7 bit ASCII text into 8 bit "
    print "HEX values like they are used in the GSM world (and vice versa)"
    print ""
    print "Valid options are:"
    print "-a\t\tconvert ASCII to HEX (PDU) format (default)"
    print "-p\t\tconvert HEX (PDU) to ASCII format"
    print "-h\t\tthis help screen"
    print ""



if __name__ == "__main__":
    main()

