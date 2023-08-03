import json

import joblib
import websocket

from classification_server import (
    predict_instance,
    transform_json_to_instance,
)

MODEL_PATH = "model.joblib"


def test_on_message():
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=lambda ws: None,
        on_message=lambda ws, message: None,
        on_error=lambda ws, error: None,
        on_close=lambda ws, close_status_code, close_msg: None,
    )

    # Create a JSON message
    json_message = {
        "Persistent": {
            "topic_name": "SIFIS:Privacy_Aware_Device_DHT_inquiry",
            "value": {
                "Dictionary": "defaultdict(<class 'int'>, {})",
                "requestor_id": "1234567890",
                "request_id": "1",
            },
        },
    }

    # Encode the JSON message
    message = json.dumps(json_message)

    # Call the on_message function
    ws.on_message(ws, message)


def test_on_error():
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=lambda ws: None,
        on_message=lambda ws, message: None,
        on_error=lambda ws, error: None,
        on_close=lambda ws, close_status_code, close_msg: None,
    )

    # Create an error message
    error = "This is an error"

    # Call the on_error function
    ws.on_error(ws, error)


def test_on_close():
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=lambda ws: None,
        on_message=lambda ws, message: None,
        on_error=lambda ws, error: None,
        on_close=lambda ws, close_status_code, close_msg: None,
    )

    # Call the on_close function
    ws.on_close(ws, 1000, "Normal closure")


def test_transform_json_to_instance():
    json_data = '{"domo_ble_thermometer": 1, "shelly_1plus": 0, "domo_switch": 1, "shelly_em": 0, "domo_power_energy_sensor": 1, "shelly_25": 0, "domo_light": 1, "shelly_1pm": 0, "domo_thermostat": 1}'
    instance = transform_json_to_instance(json_data)
    assert instance == [1, 0, 1, 0, 1, 0, 1, 0, 1]


def test_predict_instance():
    instance = [1, 0, 1, 0, 1, 0, 1, 0, 1]
    prediction = predict_instance(MODEL_PATH, instance)
    assert prediction == 0


"""
def test_receive_data():
    data = '{"request_id": "1234567890", "requestor_id": "1234567890", "dictionary": "{"domo_ble_thermometer": 1, "shelly_1plus": 0, "domo_switch": 1, "shelly_em": 0, "domo_power_energy_sensor": 1, "shelly_25": 0, "domo_light": 1, "shelly_1pm": 0, "domo_thermostat": 1}"}'
    receive_data(data)
    assert send_results.sent_results == 1
"""
