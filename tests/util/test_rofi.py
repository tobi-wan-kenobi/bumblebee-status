import unittest
from unittest.mock import MagicMock
from bumblebee_status.util.rofi import showScratchpads

class TestShowScratchpads(unittest.TestCase):
    def test_showScratchpads(self):
        global showScratchpads
        temp = showScratchpads
        showScratchpads = MagicMock()
        showScratchpads(self=None)
        showScratchpads.assert_called_once()
        showScratchpads = temp