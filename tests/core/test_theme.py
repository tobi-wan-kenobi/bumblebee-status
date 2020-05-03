import unittest
import types

import core.theme
import core.event
import core.widget


class theme(unittest.TestCase):
    def setUp(self):
        core.event.clear()
        self.invalidThemeName = "this-theme-does-not-exist"
        self.validThemeName = "default"
        self.defaultsTheme = {"defaults": {"fg": "red", "bg": "black"}}
        self.cycleTheme = {
            "cycle": [
                {"fg": "red", "bg": "black"},
                {"fg": "black", "bg": "red"},
                {"fg": "white", "bg": "blue"},
            ]
        }
        self.colorTheme = {"colors": [{"red": "#ff0000", "blue": "#0000ff"}]}
        self.walTheme = {"colors": ["wal"]}
        self.cycleValueTheme = {"defaults": {"fg": ["red", "green", "blue"]}}
        self.stateTheme = {"warning": {"fg": "yellow"}, "critical": {"fg": "red"}}

    def test_invalid_theme(self):
        with self.assertRaises(RuntimeError):
            core.theme.Theme(self.invalidThemeName)

    def test_valid_theme(self):
        theme = core.theme.Theme(self.validThemeName)
        self.assertEqual(self.validThemeName, theme.name)

    def test_defaults(self):
        theme = core.theme.Theme(raw_data=self.defaultsTheme)
        self.assertEqual(self.defaultsTheme["defaults"]["fg"], theme.get("fg"))
        self.assertEqual(self.defaultsTheme["defaults"]["bg"], theme.get("bg"))

    def test_cycle(self):
        theme = core.theme.Theme(raw_data=self.cycleTheme)
        self.assertEqual(None, theme.get("prev-bg"))
        self.assertEqual(self.cycleTheme["cycle"][0]["fg"], theme.get("fg"))
        self.assertEqual(self.cycleTheme["cycle"][0]["bg"], theme.get("bg"))
        core.event.trigger("next-widget")
        self.assertEqual(self.cycleTheme["cycle"][0]["bg"], theme.get("bg", "previous"))
        core.event.trigger("next-widget")
        self.assertEqual(self.cycleTheme["cycle"][2]["fg"], theme.get("fg"))
        self.assertEqual(self.cycleTheme["cycle"][2]["bg"], theme.get("bg"))

        with unittest.mock.patch("core.output.sys.stdout"):
            core.event.trigger("draw")
            self.assertEqual(self.cycleTheme["cycle"][0]["fg"], theme.get("fg"))
            self.assertEqual(self.cycleTheme["cycle"][0]["bg"], theme.get("bg"))

    def test_custom_iconset(self):
        theme = core.theme.Theme(raw_data=self.defaultsTheme)
        self.assertNotEqual("aaa", theme.get("padding"))
        theme = core.theme.Theme(
            raw_data=self.defaultsTheme, iconset={"defaults": {"padding": "aaa"}}
        )
        self.assertEqual("aaa", theme.get("padding"))

    def test_colors(self):
        theme = core.theme.Theme(raw_data=self.defaultsTheme)
        self.assertEqual({}, theme.keywords())
        theme = core.theme.Theme(raw_data=self.colorTheme)
        self.assertEqual(self.colorTheme["colors"][0], theme.keywords())

    def test_wal_colors(self):
        with unittest.mock.patch("core.theme.io") as io:
            with unittest.mock.patch("core.theme.os") as os:
                os.path.isfile.return_value = True
                io.open.return_value = unittest.mock.MagicMock()
                io.open.return_value.__enter__.return_value.read.return_value = """
                    { "colors": { "red": "#ff0000" } }
                """

                theme = core.theme.Theme(raw_data=self.walTheme)
                self.assertEqual({"red": "#ff0000"}, theme.keywords())

    def test_wal_special(self):
        with unittest.mock.patch("core.theme.io") as io:
            with unittest.mock.patch("core.theme.os") as os:
                os.path.isfile.return_value = True
                io.open.return_value.__enter__.return_value.read.return_value = """
                    { "special": { "background": "#ff0000" } }
                """

                theme = core.theme.Theme(raw_data=self.walTheme)
                self.assertEqual({"background": "#ff0000"}, theme.keywords())

    def test_cycle_value(self):
        widget = core.widget.Widget()
        expected = self.cycleValueTheme["defaults"]["fg"]
        theme = core.theme.Theme(raw_data=self.cycleValueTheme)

        for i in range(0, len(expected) * 3):
            self.assertEqual(expected[i % len(expected)], theme.get("fg", widget))
            self.assertEqual(
                expected[i % len(expected)], theme.get("fg", widget)
            )  # ensure multiple invocations are OK
            core.event.trigger("draw")

    def test_state(self):
        widget = core.widget.Widget()
        theme = core.theme.Theme(raw_data=self.stateTheme)

        self.assertEqual(None, theme.get("fg", widget))

        widget.state = types.MethodType(lambda self: ["warning"], widget)
        self.assertEqual(self.stateTheme["warning"]["fg"], theme.get("fg", widget))

        widget.state = types.MethodType(lambda self: ["critical"], widget)
        self.assertEqual(self.stateTheme["critical"]["fg"], theme.get("fg", widget))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
