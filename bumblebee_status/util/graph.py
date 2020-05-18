MAX_PERCENTS = 100.0


class Bar(object):
    bars = None

    def __init__(self, value):
        self.value = value


class HBar(Bar):
    bars = [
        "\u2581",
        "\u2582",
        "\u2583",
        "\u2584",
        "\u2585",
        "\u2586",
        "\u2587",
        "\u2588",
    ]

    """This class is a helper class used to draw horizontal bars - please use hbar directly

    :param value: percentage value to draw (float, between 0 and 100)
    """

    def __init__(self, value):
        super(HBar, self).__init__(value)
        self.step = MAX_PERCENTS / len(HBar.bars)

    def get_char(self):
        """Returns the character representing the current object's value

        :return: character representing the value passed during initialization
        :rtype: string with one character
        """
        for i in range(len(HBar.bars)):
            left = i * self.step
            right = (i + 1) * self.step
            if left <= self.value < right:
                return self.bars[i]
        return self.bars[-1]


def hbar(value):
    """"Retrieves the horizontal bar character representing the input value

    :param value: percentage value to draw (float, between 0 and 100)
    :return: character representing the value passed during initialization
    :rtype: string with one character
    """
    return HBar(value).get_char()


class VBar(Bar):
    bars = [
        "\u258f",
        "\u258e",
        "\u258d",
        "\u258c",
        "\u258b",
        "\u258a",
        "\u2589",
        "\u2588",
    ]

    """This class is a helper class used to draw vertical bars - please use vbar directly

    :param value: percentage value to draw (float, between 0 and 100)
    :param width: maximum width of the bar in characters
    """

    def __init__(self, value, width=1):
        super(VBar, self).__init__(value)
        self.step = MAX_PERCENTS / (len(VBar.bars) * width)
        self.width = width

    """Returns the characters representing the current object's value

    :return: characters representing the value passed during initialization
    :rtype: string
    """

    def get_chars(self):
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
    """Returns the characters representing the current object's value

    :param value: percentage value to draw (float, between 0 and 100)
    :param width: maximum width of the bar in characters

    :return: characters representing the value passed during initialization
    :rtype: string
    """
    return VBar(value, width).get_chars()


class BrailleGraph(object):
    chars = {
        (0, 0): " ",
        (1, 0): "\u2840",
        (2, 0): "\u2844",
        (3, 0): "\u2846",
        (4, 0): "\u2847",
        (0, 1): "\u2880",
        (0, 2): "\u28a0",
        (0, 3): "\u28b0",
        (0, 4): "\u28b8",
        (1, 1): "\u28c0",
        (2, 1): "\u28c4",
        (3, 1): "\u28c6",
        (4, 1): "\u28c7",
        (1, 2): "\u28e0",
        (2, 2): "\u28e4",
        (3, 2): "\u28e6",
        (4, 2): "\u28e7",
        (1, 3): "\u28f0",
        (2, 3): "\u28f4",
        (3, 3): "\u28f6",
        (4, 3): "\u28f7",
        (1, 4): "\u28f8",
        (2, 4): "\u28fc",
        (3, 4): "\u28fe",
        (4, 4): "\u28ff",
    }

    """This class is a helper class used to draw braille graphs - please use braille directly

    :param values: values to draw
    """

    def __init__(self, values):
        self.values = values
        # length of values list must be even
        # because one Braille char displays two values
        if len(self.values) % 2 == 1:
            self.values.append(0)
        self.steps = self.get_steps()
        self.parts = [tuple(self.steps[i : i + 2]) for i in range(len(self.steps))[::2]]

    @staticmethod
    def get_height(value, unit):
        if value < unit / 10.0:
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
        maxval = max(self.values)
        unit = maxval / 4.0
        if unit == 0:
            return [0] * len(self.values)
        stepslist = []
        for value in self.values:
            stepslist.append(self.get_height(value, unit))
        return stepslist

    def get_chars(self):
        chars = []
        for part in self.parts:
            chars.append(BrailleGraph.chars[part])
        return "".join(chars)


def braille(values):
    return BrailleGraph(values).get_chars()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
