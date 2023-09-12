import json

import classification_server
import websocket


def on_message(ws, message):
    print("Received: " + message)

    json_message = json.loads(message)

    if "Persistent" in json_message:
        json_message = json_message["Persistent"]
        topic_name = json_message["topic_name"]
        # handle topic name
        if topic_name == "SIFIS:Privacy_Aware_Device_DHT_inquiry":
            if "value" in json_message:
                json_message = json_message["value"]
                dictionary = json_message["Dictionary"]
                requestor_id = json_message["requestor_id"]
                request_id = json_message["request_id"]
                try:
                    new_dictionary = dictionary.split(
                        "defaultdict(<class 'int'>, ", 1
                    )[1]
                except:
                    new_dictionary = dictionary.replace("'", '"')
                data = {
                    "requestor_id": requestor_id,
                    "request_id": request_id,
                    "dictionary": new_dictionary,
                }
                response = classification_server.receive_data(str(data))
                print(response)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
