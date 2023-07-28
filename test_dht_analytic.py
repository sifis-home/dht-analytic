from unittest.mock import patch

import pytest

import catch_dht_inquiry


@pytest.fixture
def mock_receive_data():
    with patch("classification_server.receive_data") as mock_receive_data:
        yield mock_receive_data


"""
def test_on_message(mock_receive_data):
    ws = MagicMock()
    message = '{"Persistent": {"topic_name": "SIFIS:Privacy_Aware_Device_DHT_inquiry", "value": {"Dictionary": "defaultdict(<class \'int\'>, {1: 100, 2: 200})", "requestor_id": "some_requestor_id", "request_id": "some_request_id"}}}'

    # Call the on_message function with the mock WebSocket and message
    catch_dht_inquiry.on_message(ws, message)

    # Convert the received dictionary string to an actual dictionary
    expected_dict_str = "defaultdict(<class 'int'>, {1: 100, 2: 200})"
    expected_data = {
        "requestor_id": "some_requestor_id",
        "request_id": "some_request_id",
        "dictionary": ast.literal_eval(expected_dict_str),
    }

    # Assert that classification_server.receive_data() is called with the correct data
    mock_receive_data.assert_called_once_with(expected_data)
"""


def test_on_error():
    error = "WebSocket error occurred"

    with patch("builtins.print") as mock_print:
        catch_dht_inquiry.on_error(None, error)

    mock_print.assert_called_once_with(error)


def test_on_close():
    close_status_code = 1000
    close_msg = "Connection closed"

    with patch("builtins.print") as mock_print:
        catch_dht_inquiry.on_close(None, close_status_code, close_msg)

    mock_print.assert_called_once_with("### Connection closed ###")


def test_on_open():
    with patch("builtins.print") as mock_print:
        catch_dht_inquiry.on_open(None)

    mock_print.assert_called_once_with("### Connection established ###")
