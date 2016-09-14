'''
Created on 12.09.2016

@author: hannayk
'''
import os
import unittest
from mock import call, patch, MagicMock

import common

class Test(unittest.TestCase):


    @patch("__builtin__.open")
    def testGetEfaLivePlatformPc(self, open_mock):
        os.path.exists = MagicMock(return_value = True)
        open_mock.return_value = FileStub(common.Platform.PC)

        result = common.get_efalive_platform()

        self.assertEqual(result, common.Platform.PC)

    @patch("__builtin__.open")
    def testGetEfaLivePlatformRaspi(self, open_mock):
        os.path.exists = MagicMock(return_value = True)
        open_mock.return_value = FileStub(common.Platform.RASPI)

        result = common.get_efalive_platform()

        self.assertEqual(result, common.Platform.RASPI)

    @patch("__builtin__.open")
    def testGetEfaLivePlatformNoFile(self, open_mock):
        os.path.exists = MagicMock(return_value = False)

        result = common.get_efalive_platform()

        self.assertEqual(result, common.Platform.PC)

class FileStub(object):

    def __init__(self, platform):
        if platform == common.Platform.RASPI:
            self.settings_list = [
                    "PRETTY_NAME=\"Raspbian GNU/Linux 8 (jessie)\"",
                    "NAME=\"Raspbian GNU/Linux\"",
                    "VERSION_ID=\"8\"",
                    "VERSION=\"8 (jessie)\"",
                    "ID=raspbian",
                    "ID_LIKE=debian",
                    "HOME_URL=\"http://www.raspbian.org/\"",
                    "SUPPORT_URL=\"http://www.raspbian.org/RaspbianForums\"",
                    "BUG_REPORT_URL=\"http://www.raspbian.org/RaspbianBugs\"",
                    ]
        else:
            self.settings_list = [
                    "PRETTY_NAME=\"Debian GNU/Linux stretch/sid\"",
                    "NAME=\"Debian GNU/Linux\"",
                    "ID=debian",
                    "HOME_URL=\"https://www.debian.org/\"",
                    "SUPPORT_URL=\"https://www.debian.org/support\""
                    "BUG_REPORT_URL=\"https://bugs.debian.org/\"",
                    ]

    def close(self):
        pass

    def __iter__(self):
        return iter(self.settings_list)

    def write(self, data):
        self.settings_list.append(data)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetEfaLiveVarintPc']
    unittest.main()