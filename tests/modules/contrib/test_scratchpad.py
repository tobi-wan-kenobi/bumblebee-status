import pytest

from bumblebee_status.modules.contrib.scratchpad import Module
from modules.contrib.scratchpad import Module
from unittest.mock import MagicMock, patch
from unittest.mock import Mock, patch
from util.rofi import showScratchpads
import core.input
import core.module
import core.widget
import i3ipc
import sys
import threading

def test_load_module():
    __import__("modules.contrib.scratchpad")


class TestScratchpad:

    def test___getTitle_1(self):
        """
        Test that __getTitle method returns the correct title.

        This test verifies that the __getTitle method of the Module class
        returns the value of the __title attribute without modification.
        """
        config = {}
        theme = {}
        module = Module(config, theme)
        module._Module__title = "Test Title"

        result = module._Module__getTitle(None)

        assert result == "Test Title"

    def test___pollScratchpads_2(self):
        """
        Test the __pollScratchpads method when scratchpad exists and count is different from self.__scratchpads.

        This test verifies that when a scratchpad is found and the number of floating nodes
        is different from the current scratchpad count, the method updates the scratchpad count
        and sets the title to the new count.
        """
        config = MagicMock()
        theme = MagicMock()
        module = Module(config, theme)

        # Mock i3ipc.Connection and its methods
        mock_i3 = MagicMock()
        mock_root = MagicMock()
        mock_scratchpad = MagicMock()
        mock_scratchpad.floating_nodes = [MagicMock(), MagicMock()]  # Two floating nodes

        mock_i3.get_tree.return_value = mock_root
        mock_root.scratchpad.return_value = mock_scratchpad

        module._Module__i3 = mock_i3
        module._Module__scratchpads = 0  # Initial count different from the mock

        # Call the method
        module._Module__pollScratchpads()

        # Assert the results
        assert module._Module__scratchpads == 2
        assert module._Module__title == "2"

    def test___pollScratchpads_3(self):
        """
        Test the __pollScratchpads method when a scratchpad exists but the count hasn't changed.
        This test covers the path where the scratchpad is found, but the number of scratchpads
        remains the same as the previous count.
        """
        config = MagicMock()
        theme = MagicMock()
        module = Module(config, theme)

        # Mock i3ipc Connection and Tree
        mock_i3 = MagicMock()
        mock_root = MagicMock()
        mock_scratchpad = MagicMock()

        module._Module__i3 = mock_i3
        mock_i3.get_tree.return_value = mock_root
        mock_root.scratchpad.return_value = mock_scratchpad

        # Set up the scratchpad to have floating nodes
        mock_scratchpad.floating_nodes = [MagicMock(), MagicMock()]

        # Set the initial scratchpad count
        module._Module__scratchpads = 2
        module._Module__title = "2"

        # Call the method
        module._Module__pollScratchpads()

        # Assert that the title and count haven't changed
        assert module._Module__scratchpads == 2
        assert module._Module__title == "2"


    def test___pollScratchpads_no_scratchpad_2(self):
        """
        Test the __pollScratchpads method when no scratchpad is found.
        This test verifies that the method correctly updates the internal state
        when the i3 tree does not contain a scratchpad.
        """
        mock_config = Mock()
        mock_theme = Mock()

        with patch('i3ipc.Connection') as mock_i3ipc:
            mock_root = Mock()
            mock_root.scratchpad.return_value = None
            mock_i3ipc.return_value.get_tree.return_value = mock_root

            module = Module(mock_config, mock_theme)
            module._Module__pollScratchpads()

            assert module._Module__scratchpads == 0
            assert module._Module__title == "No scratchpad found"

    def test_load_module(self):
        __import__("modules.contrib.scratchpad")



def test___init___1():
    """
    Test the initialization of the Module class in the scratchpad module.

    This test verifies that the Module is correctly initialized with the given
    config and theme, sets up the widget, registers input, initializes the
    scratchpad count, creates an i3ipc connection, and starts a thread for
    listening to events.
    """
    config = MagicMock()
    theme = MagicMock()

    with patch('i3ipc.Connection') as mock_i3ipc, \
         patch('threading.Thread') as mock_thread, \
         patch('util.rofi.showScratchpads') as mock_show_scratchpads:

        mock_i3 = MagicMock()
        mock_i3ipc.return_value = mock_i3

        module = Module(config, theme)

        assert isinstance(module, core.module.Module)
        assert module._Module__scratchpads == 0
        assert module._Module__title == "0"
        mock_i3ipc.assert_called_once()
        assert mock_i3.on.call_count == 2
        mock_thread.assert_called_once_with(target=mock_i3.main)
        mock_thread.return_value.start.assert_called_once()