import json

import joblib
import requests

import send_results

MODEL_PATH = "model.joblib"

url = "http://localhost:3000/"


def transform_json_to_instance(json_data):
    # Converti la stringa JSON in un dizionario Python
    data_dict = json.loads(json_data)
    # data_dict = eval(data_dict)
    # Definisci l'ordine degli attributi
    attributes = [
        "domo_ble_thermometer",
        "shelly_1plus",
        "domo_switch",
        "shelly_em",
        "domo_power_energy_sensor",
        "shelly_25",
        "domo_light",
        "shelly_1pm",
        "domo_thermostat",
    ]
    # Crea una lista vuota per l'istanza
    instance = []
    # Per ogni attributo nell'ordine definito sopra, aggiungi il valore corrispondente alla lista
    for attribute in attributes:
        value = data_dict.get(attribute, 0)
        instance.append(value)
    # Restituisci l'istanza come lista
    return instance


def predict_instance(model_path, instance_json):
    # instance = transform_json_to_instance(instance_json)
    model = joblib.load(model_path)
    prediction = model.predict([instance_json])
    return prediction[0]


def receive_data(received_data):
    print("received_data: ")
    print(receive_data)
    data = eval(received_data)
    request_id = data.get("request_id", None)
    requestor_id = data.get("requestor_id", None)
    dictionary = data.get("dictionary", None)
    print("DICTIONARY")
    print(dictionary)
    try:
        dictionary = dictionary.replace(")", "")
        dictionary = dictionary.replace("'", '"')
        handle_dictionary(data, dictionary, request_id, requestor_id)
    except Exception as e:
        print(e)
        pass


def send_results(result_data):
    topic_uuid = "DHT_inquiry_results"
    topic_name = "SIFIS:Privacy_Aware_Device_DHT_Results"
    requests.post(
        url + "topic_name/" + topic_name + "/topic_uuid/" + topic_uuid,
        json=result_data,
    )


def handle_dictionary(data, dictionary, request_id, requestor_id):
    print("Received: " + str(dictionary))
    instance = transform_json_to_instance(dictionary)
    prediction = predict_instance(MODEL_PATH, instance)
    {"instance": data, "prediction": str(prediction)}
    for elem in str(prediction):
        if elem == "1":
            response = "System Violation"
            print("System Violation")
        elif elem == "0":
            response = "Correct Invocation"
            print("Correct Invocation")
        data = {
            "request_id": request_id,
            "requestor_id": requestor_id,
            "data": str(data),
            "response": response,
        }
        send_results(data)
        return
