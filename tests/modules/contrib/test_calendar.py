import pytest
from bumblebee_status.modules.contrib.calendar import Module, get_default_browser_linux
from unittest.mock import MagicMock, patch
from unittest import mock, TestCase
from freezegun import freeze_time

import core.config
import core.input
import core.widget
import modules.core.datetime

pytest.importorskip("datetime")

def test_load_module():
    __import__("modules.contrib.calendar")

# Mocking os.popen
@pytest.fixture
def mock_popen(mocker):
    return mocker.patch('os.popen')


def test_get_default_browser_linux_valid_browser(mock_popen):
    # Simulate a valid browser ID with ".desktop"
    mock_popen.return_value.read.return_value = 'firefox.desktop\n'
    
    # Call the function
    result = get_default_browser_linux()
    
    # Assert the result after stripping '.desktop'
    assert result == 'firefox'


def test_get_default_browser_linux_no_browser(mock_popen):
    # Simulate the case where no browser is set (empty string)
    mock_popen.return_value.read.return_value = ''
    
    # Call the function
    result = get_default_browser_linux()
    
    # Assert the result is None
    assert result is None


def test_get_default_browser_linux_invalid_browser(mock_popen):
    # Simulate a browser ID without ".desktop" (invalid case)
    mock_popen.return_value.read.return_value = 'firefox\n'
    
    # Call the function
    result = get_default_browser_linux()
    
    # Assert the result is the browser ID as it is
    assert result == 'firefox'


def test_get_default_browser_linux_exception(mock_popen):
    # Simulate an exception during the command execution
    mock_popen.side_effect = Exception("Command failed")
    
    # Call the function
    result = get_default_browser_linux()
    
    # Assert the result is None due to exception
    assert result is None

@pytest.fixture
def module():
    config = {}
    theme = {}
    mock_dtlibrary = MagicMock()
    return Module(config, theme, dtlibrary=mock_dtlibrary)
    
# Test for display_calendar method (opening browser)
@patch('subprocess.Popen')
@patch('tkinter.Tk')
@patch('tkcalendar.Calendar')
@patch('modules.contrib.calendar.get_default_browser_linux', return_value='/usr/bin/firefox')
def test_display_calendar(mock_get_browser, mock_Calendar, mock_Tk, mock_popen, module):
    # Mock tkinter methods
    mock_root = MagicMock()
    mock_Tk.return_value = mock_root
    mock_cal = MagicMock()
    mock_Calendar.return_value = mock_cal
    # Mock parameter calls
    module.parameter = MagicMock(browserpath='/usr/bin/firefox')
    # Run display_calendar
    module.display_calendar(None)
    # Assertions for tkinter window and calendar creation
    mock_Tk.assert_called_once()
    mock_Calendar.assert_called_once()
    # Check if subprocess.Popen is called with correct parameters
    mock_popen.assert_called_once()