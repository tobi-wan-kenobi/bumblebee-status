from bumblebee_status.util.rofi import showScratchpads
from rofi import Rofi
from unittest.mock import patch, MagicMock
import i3ipc
import unittest

class TestRofi(unittest.TestCase):

    def showScratchpads(self):
        i3 = i3ipc.Connection()
        scratchpad_windows = []
        for leaf in i3.get_tree().scratchpad().leaves():
            scratchpad_windows.append(leaf)

        if len(scratchpad_windows):
            #  sort by window's name
            scratchpad_windows = sorted(scratchpad_windows, key=lambda x: x.ipc_data['name'])
            r = Rofi()
            scratchpad_windows_name = list(map(lambda x: x.ipc_data['name'], scratchpad_windows))
            index, _ = r.select('Select Window in Scratchpad', scratchpad_windows_name)

            # select == -1 means nothing select
            if index != -1:
                scratchpad_windows[index].command('focus')


    def test_showScratchpads(self):
        """
        Test showScratchpads when scratchpad windows exist but no window is selected.

        This test verifies that when there are scratchpad windows available,
        but the user doesn't select any window (Rofi returns -1), no focus
        command is issued.
        """
        with patch('i3ipc.Connection') as mock_i3_connection, \
             patch('rofi.Rofi') as mock_rofi:

            # Mock i3ipc.Connection
            mock_i3 = MagicMock()
            mock_i3_connection.return_value = mock_i3
            mock_tree = MagicMock()
            mock_i3.get_tree.return_value = mock_tree
            mock_scratchpad = MagicMock()
            mock_tree.scratchpad.return_value = mock_scratchpad

            # Create mock scratchpad windows
            mock_window1 = MagicMock()
            mock_window1.ipc_data = {'name': 'Window 1'}
            mock_window2 = MagicMock()
            mock_window2.ipc_data = {'name': 'Window 2'}
            mock_scratchpad.leaves.return_value = [mock_window1, mock_window2]

            # Mock Rofi
            mock_rofi_instance = MagicMock()
            mock_rofi.return_value = mock_rofi_instance
            mock_rofi_instance.select.return_value = (-1, None)  # Simulate no selection

            # Call the method under test
            showScratchpads(None)

            # Verify that no focus command was issued
            mock_window1.command.assert_not_called()
            mock_window2.command.assert_not_called()

    def test_showScratchpads_no_scratchpad_windows(self):
        """
        Test the behavior of showScratchpads when there are no scratchpad windows.
        This tests the edge case where the scratchpad_windows list is empty.
        """
        rofi = TestRofi()

        # Mock i3ipc.Connection to return an empty scratchpad
        class MockI3:
            def get_tree(self):
                return self
            def scratchpad(self):
                return self
            def leaves(self):
                return []

        i3ipc.Connection = lambda: MockI3()

        # Call the method
        result = rofi.showScratchpads()

        # Assert that the method returns None (implicit return)
        assert result is None

    def test_showScratchpads_user_cancels_selection(self):
        """
        Test the behavior of showScratchpads when the user cancels the window selection.
        This tests the edge case where the Rofi selection returns -1.
        """
        rofi = TestRofi()

        # Mock i3ipc.Connection to return some scratchpad windows
        class MockWindow:
            def __init__(self, name):
                self.ipc_data = {'name': name}

        class MockI3:
            def get_tree(self):
                return self
            def scratchpad(self):
                return self
            def leaves(self):
                return [MockWindow("Window1"), MockWindow("Window2")]

        i3ipc.Connection = lambda: MockI3()

        # Mock Rofi to simulate user cancellation
        class MockRofi:
            def select(self, prompt, options):
                return -1, None

        Rofi = MockRofi

        # Call the method
        result = rofi.showScratchpads()

        # Assert that the method returns None (implicit return)
        assert result is None

    def test_showScratchpads_when_no_scratchpad_windows(self):
        """
        Test showScratchpads when there are no scratchpad windows.
        This test verifies that the method handles the case where
        no scratchpad windows are found correctly.
        """
        with patch('i3ipc.Connection') as mock_connection:
            mock_i3 = MagicMock()
            mock_connection.return_value = mock_i3
            mock_tree = MagicMock()
            mock_i3.get_tree.return_value = mock_tree
            mock_scratchpad = MagicMock()
            mock_tree.scratchpad.return_value = mock_scratchpad
            mock_scratchpad.leaves.return_value = []

            showScratchpads(self)

            mock_connection.assert_called_once()
            mock_i3.get_tree.assert_called_once()
            mock_tree.scratchpad.assert_called_once()
            mock_scratchpad.leaves.assert_called_once()
