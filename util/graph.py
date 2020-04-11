MAX_PERCENTS = 100.

class Bar(object):
    """superclass"""
    bars = None

    def __init__(self, value):
        """
            Args:

                value (float): value between 0. and 100. meaning percents
        """
        self.value = value

class HBar(Bar):
    """horizontal bar (1 char)"""
    bars = [
        u"\u2581",
        u"\u2582",
        u"\u2583",
        u"\u2584",
        u"\u2585",
        u"\u2586",
        u"\u2587",
        u"\u2588"
    ]

    def __init__(self, value):
        """
            Args:

                value (float): value between 0. and 100. meaning percents
        """
        super(HBar, self).__init__(value)
        self.step = MAX_PERCENTS / len(HBar.bars)

    def get_char(self):
        """
            Decide which char to draw

            Return: str
        """
        for i in range(len(HBar.bars)):
            left = i * self.step
            right = (i + 1) * self.step
            if left <= self.value < right:
                return self.bars[i]
        return self.bars[-1]

def hbar(value):
    """wrapper function"""
    return HBar(value).get_char()


class VBar(Bar):
    """vertical bar (can be more than 1 char)"""
    bars = [
        u"\u258f",
        u"\u258e",
        u"\u258d",
        u"\u258c",
        u"\u258b",
        u"\u258a",
        u"\u2589",
        u"\u2588"
    ]

    def __init__(self, value, width=1):
        """
            Args:

                value (float): value between 0. and 100. meaning percents

                width (int): width
        """
        super(VBar, self).__init__(value)
        self.step = MAX_PERCENTS / (len(VBar.bars) * width)
        self.width = width

    def get_chars(self):
        """
            Decide which char to draw

            Return: str
        """
        if self.value == 100:
            return self.bars[-1] * self.width
        if self.width == 1:
            for i in range(len(VBar.bars)):
                left = i * self.step
                right = (i + 1) * self.step
                if left <= self.value < right:
                    return self.bars[i]
        else:
            full_parts = int(self.value // (self.step * len(Vbar.bars)))
            remainder = self.value - full_parts * self.step * CHARS
            empty_parts = self.width - full_parts
            if remainder >= 0:
                empty_parts -= 1
            part_vbar = VBar(remainder * self.width)  # scale to width
            chars = self.bars[-1] * full_parts
            chars += part_vbar.get_chars()
            chars += " " * empty_parts
            return chars


def vbar(value, width):
    """wrapper function"""
    return VBar(value, width).get_chars()

class BrailleGraph(object):
    """
        graph using Braille chars
        scaled to passed values
    """
    chars = {
        (0, 0): u" ",
        (1, 0): u"\u2840",
        (2, 0): u"\u2844",
        (3, 0): u"\u2846",
        (4, 0): u"\u2847",
        (0, 1): u"\u2880",
        (0, 2): u"\u28a0",
        (0, 3): u"\u28b0",
        (0, 4): u"\u28b8",
        (1, 1): u"\u28c0",
        (2, 1): u"\u28c4",
        (3, 1): u"\u28c6",
        (4, 1): u"\u28c7",
        (1, 2): u"\u28e0",
        (2, 2): u"\u28e4",
        (3, 2): u"\u28e6",
        (4, 2): u"\u28e7",
        (1, 3): u"\u28f0",
        (2, 3): u"\u28f4",
        (3, 3): u"\u28f6",
        (4, 3): u"\u28f7",
        (1, 4): u"\u28f8",
        (2, 4): u"\u28fc",
        (3, 4): u"\u28fe",
        (4, 4): u"\u28ff"
    }
    def __init__(self, values):
        """
            Args:

                values (list): list of values
        """
        self.values = values
        # length of values list must be even
        # because one Braille char displays two values
        if len(self.values) % 2 == 1:
            self.values.append(0)
        self.steps = self.get_steps()
        self.parts = [tuple(self.steps[i:i+2])
                      for i in range(len(self.steps))[::2]]

    @staticmethod
    def get_height(value, unit):
        """
            Compute height of a value relative to unit

            Args:

                value (number): value

                unit (number): unit
        """
        if value < unit / 10.:
            return 0
        elif value <= unit:
            return 1
        elif value <= unit * 2:
            return 2
        elif value <= unit * 3:
            return 3
        else:
            return 4

    def get_steps(self):
        """
            Convert the list of values to a list of steps

            Return: list
        """
        maxval = max(self.values)
        unit = maxval / 4.
        if unit == 0:
            return [0] * len(self.values)
        stepslist = []
        for value in self.values:
            stepslist.append(self.get_height(value, unit))
        return stepslist

    def get_chars(self):
        """
            Decide which chars to draw

            Return: str
        """
        chars = []
        for part in self.parts:
            chars.append(BrailleGraph.chars[part])
        return "".join(chars)

def braille(values):
    """wrapper function"""
    return BrailleGraph(values).get_chars()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
