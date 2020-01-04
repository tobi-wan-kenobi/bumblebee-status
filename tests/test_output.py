import unittest

import bumblebee.output


class TestHBar(unittest.TestCase):
    """tests for bumblebee.output.HBar"""
    def setUp(self):
        self.value = 1
        self.values = [10, 20, 30, 40, 55, 65, 80, 90]
        self.hbar = bumblebee.output.HBar(self.value)

    def test___init__(self):
        """bumblebee.output.HBar.__init__()"""
        self.assertEqual(
            self.hbar.step, bumblebee.output.MAX_PERCENTS / bumblebee.output.CHARS)

    def test_get_char(self):
        """bumblebee.output.HBar.get_char()"""
        for i in range(bumblebee.output.CHARS):
            hbar = bumblebee.output.HBar(self.values[i])
            self.assertEqual(hbar.get_char(), bumblebee.output.HBARS[i])
        # edge case for 100%
        hbar = bumblebee.output.HBar(100)
        self.assertEqual(hbar.get_char(), bumblebee.output.HBARS[-1])


class TestVBar(unittest.TestCase):
    """tests for bumblebee.output.VBar"""
    def setUp(self):
        self.value = 1
        self.values = [10, 20, 30, 40, 55, 65, 80, 90]
        self.vbar = bumblebee.output.VBar(self.value)

    def test___init__(self):
        """bumblebee.output.VBar.__init__()"""
        self.assertEqual(
            self.vbar.step, bumblebee.output.MAX_PERCENTS / bumblebee.output.CHARS)

    def test_get_chars(self):
        """bumblebee.output.VBar.get_char()"""
        for i in range(bumblebee.output.CHARS):
            vbar = bumblebee.output.VBar(self.values[i])
            self.assertEqual(vbar.get_chars(), bumblebee.output.VBARS[i])
        # edge case for 100%
        vbar = bumblebee.output.VBar(100)
        self.assertEqual(vbar.get_chars(), bumblebee.output.VBARS[-1])
        # 0.x chars filled
        value = 0.1
        vbar = bumblebee.output.VBar(value, 3)
        expected_chars = vbar.bars[0] + "  "
        self.assertEqual(vbar.get_chars(), expected_chars)
        # 1.x chars filled
        value = 35
        vbar = bumblebee.output.VBar(value, 3)
        expected_chars = vbar.bars[-1] + vbar.bars[0] + " "
        self.assertEqual(vbar.get_chars(), expected_chars)
        # 2.x chars filled
        value = 67
        vbar = bumblebee.output.VBar(value, 3)
        expected_chars = vbar.bars[-1] * 2 + vbar.bars[0]
        self.assertEqual(vbar.get_chars(), expected_chars)
