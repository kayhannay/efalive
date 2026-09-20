"""
Created on 12.09.2016

@author: hannayk
"""

import os
import unittest
from unittest.mock import patch, MagicMock, mock_open

import efalive.common.common as common


class Test(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def testGetEfaLivePlatformPc(self, open_mock):
        os.path.exists = MagicMock(return_value=False)

        result = common.get_efalive_platform()

        self.assertEqual(result, common.Platform.PC)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def testGetEfaLivePlatformRaspi(self, open_mock):
        os.path.exists = MagicMock(return_value=True)

        result = common.get_efalive_platform()

        self.assertEqual(result, common.Platform.RASPI)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testGetEfaLiveVarintPc']
    unittest.main()

