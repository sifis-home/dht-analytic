import json
import threading
import time

import websocket


def publish_thread(request_id, requestor_id, dictionary, system_response):
    ws = websocket.WebSocketApp(
        "ws://sifis-device3.iit.cnr.it:3000/ws",
        on_open=on_open,
        on_error=on_error,
        on_close=on_close,
    )

    def send_data():
        ws_req = {
            "RequestPostTopicUUID": {
                "topic_name": "SIFIS:Privacy_Aware_Device_DHT_Results",
                "topic_uuid": "DHT_inquiry_results",
                "value": {
                    "description": "DHT inquiry results",
                    "requestor_id": str(requestor_id),
                    "request_id": str(request_id),
                    "connected": True,
                    "Data Type": "String",
                    "Response": str(system_response),
                    "Dictionary": str(dictionary),
                },
            }
        }
        time.sleep(5)
        ws.send(json.dumps(ws_req))

    def keep_sending_data():
        while True:
            if ws.sock and ws.sock.connected:
                send_data()
            else:
                print("Websocket not connected, waiting for reconnection...")
                time.sleep(1)

    # Start the thread that sends data periodically
    data_thread = threading.Thread(target=keep_sending_data)
    data_thread.start()

    # Start the websocket connection
    ws.run_forever()  # Remove dispatcher parameter as it's not necessary anymore


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


def send_results(request_id, requestor_id, dictionary, system_response):
    # Start a new thread to publish the data
    publish_data = threading.Thread(
        target=publish_thread,
        args=(
            request_id,
            requestor_id,
            dictionary,
            system_response,
        ),
    )
    publish_data.start()

    return "Data Sent"
