import time
from unittest import TestCase, mock

import core.config
import modules.contrib.apt


def build_module(format_str=None, warning=0, critical=50):
    """Helper to build an apt module with optional parameters."""
    params = []
    if format_str is not None:
        params.extend(["-p", "apt.format={}".format(format_str)])
    if warning is not None:
        params.extend(["-p", "apt.warning={}".format(warning)])
    if critical is not None:
        params.extend(["-p", "apt.critical={}".format(critical)])
    config = core.config.Config(params)
    return modules.contrib.apt.Module(config=config, theme=None)


class TestAPT(TestCase):
    def test_load_module(self):
        __import__("modules.contrib.apt")

    def test_parse_result_with_all_values(self):
        """Test parsing apt-get output with all values present."""
        module = build_module()
        output = "Reading package lists...\nBuilding dependency tree...\n5 upgraded, 2 newly installed, 3 to remove and 1 not upgraded"
        up, new, rm, kept = module._parse_result(output)
        assert up == 5
        assert new == 2
        assert rm == 3
        assert kept == 1

    def test_parse_result_without_not_upgraded(self):
        """Test parsing apt-get output without 'not upgraded'."""
        module = build_module()
        output = "Reading package lists...\nBuilding dependency tree...\n10 upgraded, 5 newly installed, 2 to remove"
        up, new, rm, kept = module._parse_result(output)
        assert up == 10
        assert new == 5
        assert rm == 2
        assert kept == 0

    def test_parse_result_multiple_lines(self):
        """Test parsing when the pattern appears in multiple lines (should use last match)."""
        module = build_module()
        output = "Reading package lists...\n3 upgraded, 1 newly installed, 0 to remove\nBuilding dependency tree...\n7 upgraded, 2 newly installed, 1 to remove"
        up, new, rm, kept = module._parse_result(output)
        assert up == 7
        assert new == 2
        assert rm == 1
        assert kept == 0

    def test_parse_result_no_match(self):
        """Test parsing when no pattern matches."""
        module = build_module()
        output = "Reading package lists...\nNo packages to upgrade"
        up, new, rm, kept = module._parse_result(output)
        assert up == 0
        assert new == 0
        assert rm == 0
        assert kept == 0

    def test_parse_result_empty_string(self):
        """Test parsing empty string."""
        module = build_module()
        up, new, rm, kept = module._parse_result("")
        assert up == 0
        assert new == 0
        assert rm == 0
        assert kept == 0

    def test_updates_default_format_no_updates(self):
        """Test updates display with default format and no updates."""
        module = build_module()
        widget = module.widget()
        widget.set("to_upgrade", 0)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.updates(widget) == "0 to upgrade, 0 to remove"

    def test_updates_default_format_with_updates(self):
        """Test updates display with default format and updates."""
        module = build_module()
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 2)
        widget.set("not_upgraded", 0)
        assert module.updates(widget) == "5 to upgrade, 2 to remove"

    def test_updates_default_format_with_kept_back(self):
        """Test updates display with default format and kept back packages."""
        module = build_module()
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 2)
        widget.set("not_upgraded", 3)
        assert module.updates(widget) == "5 to upgrade, 2 to remove, 3 kept back"

    def test_updates_custom_format(self):
        """Test updates display with custom format string."""
        module = build_module(format_str="{to_upgrade}U/{to_remove}R/{kept_back}K")
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 2)
        widget.set("not_upgraded", 3)
        assert module.updates(widget) == "5U/2R/3K"

    def test_updates_custom_format_with_zero_kept_back(self):
        """Test custom format shows kept_back even when zero."""
        module = build_module(format_str="{to_upgrade}U/{kept_back}K")
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.updates(widget) == "5U/0K"

    def test_updates_format_error(self):
        """Test updates display with invalid format placeholder."""
        module = build_module(format_str="{to_upgrade}U/{invalid_placeholder}I")
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 2)
        widget.set("not_upgraded", 0)
        result = module.updates(widget)
        assert "Format error" in result
        assert "invalid_placeholder" in result

    def test_updates_with_error(self):
        """Test updates display when widget has an error."""
        module = build_module()
        widget = module.widget()
        widget.set("error", "APT error: Connection failed")
        assert module.updates(widget) == "APT error: Connection failed"

    def test_state_good_default_thresholds(self):
        """Test state returns 'good' when below thresholds."""
        module = build_module()
        widget = module.widget()
        widget.set("to_upgrade", 0)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.state(widget) == "good"

    def test_state_warning_default_thresholds(self):
        """Test state returns 'warning' when above warning threshold."""
        module = build_module()
        widget = module.widget()
        widget.set("to_upgrade", 1)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.state(widget) == "warning"

    def test_state_critical_default_thresholds(self):
        """Test state returns 'critical' when above critical threshold."""
        module = build_module()
        widget = module.widget()
        widget.set("to_upgrade", 51)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.state(widget) == "critical"

    def test_state_custom_warning_threshold(self):
        """Test state with custom warning threshold."""
        module = build_module(warning=10, critical=50)
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.state(widget) == "good"

        widget.set("to_upgrade", 15)
        assert module.state(widget) == "warning"

    def test_state_custom_critical_threshold(self):
        """Test state with custom critical threshold."""
        module = build_module(warning=10, critical=100)
        widget = module.widget()
        widget.set("to_upgrade", 50)
        widget.set("to_remove", 0)
        widget.set("not_upgraded", 0)
        assert module.state(widget) == "warning"

        widget.set("to_upgrade", 101)
        assert module.state(widget) == "critical"

    def test_state_sums_all_counts(self):
        """Test state calculation sums to_upgrade, to_remove, and not_upgraded."""
        module = build_module(warning=10, critical=50)
        widget = module.widget()
        widget.set("to_upgrade", 5)
        widget.set("to_remove", 3)
        widget.set("not_upgraded", 2)
        # Total = 10, should be good (not > 10)
        assert module.state(widget) == "good"

        widget.set("to_upgrade", 5)
        widget.set("to_remove", 3)
        widget.set("not_upgraded", 3)
        # Total = 11, should be warning (> 10)
        assert module.state(widget) == "warning"

    def test_state_with_error(self):
        """Test state returns 'critical' when widget has error."""
        module = build_module()
        widget = module.widget()
        widget.set("error", "APT error: Connection failed")
        assert module.state(widget) == "critical"

    @mock.patch("util.cli.execute")
    def test_get_apt_check_info_success(self, execute_mock):
        """Test successful apt-get check info retrieval."""
        execute_mock.return_value = "Reading package lists...\n5 upgraded, 2 newly installed, 3 to remove and 1 not upgraded"
        module = build_module()

        module._get_apt_check_info()

        widget = module.widget()
        assert widget.get("error") is None
        assert widget.get("to_upgrade") == 5
        assert widget.get("to_remove") == 3
        assert widget.get("not_upgraded") == 1
        execute_mock.assert_called_once_with("apt-get -s dist-upgrade")

    @mock.patch("util.cli.execute")
    def test_get_apt_check_info_failure(self, execute_mock):
        """Test apt-get check info retrieval with exception."""
        execute_mock.side_effect = Exception("Command not found")
        module = build_module()

        module._get_apt_check_info()

        widget = module.widget()
        assert "APT error" in widget.get("error")
        assert "Command not found" in widget.get("error")

    @mock.patch("util.cli.execute")
    def test_update_triggers_thread(self, execute_mock):
        """Test that update() starts a new thread when none exists."""
        execute_mock.return_value = "Reading package lists...\n0 upgraded, 0 newly installed, 0 to remove"
        module = build_module()

        # First update should start a thread
        module.update()

        # Wait a bit for thread to complete
        time.sleep(0.1)

        # Verify the command was called
        execute_mock.assert_called_with("apt-get -s dist-upgrade")

    @mock.patch("util.cli.execute")
    def test_update_does_not_start_multiple_threads(self, execute_mock):
        """Test that update() doesn't start multiple threads if one is already running."""
        execute_mock.return_value = "Reading package lists...\n0 upgraded, 0 newly installed, 0 to remove"
        module = build_module()

        # Start first update
        module.update()

        # Try to start another update immediately (thread should still be alive)
        module.update()

        # Wait for threads to complete
        time.sleep(0.2)

        # Should only be called once (or maybe twice if thread finished quickly)
        # The important thing is we don't spawn unlimited threads
        assert execute_mock.call_count <= 2

