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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
