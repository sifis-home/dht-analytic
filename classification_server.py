import json

import joblib

import send_results

MODEL_PATH = "model.joblib"


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


def receive_data(data):
    data = eval(data)
    request_id = data.get("request_id", None)
    requestor_id = data.get("requestor_id", None)
    dictionary = data.get("dictionary", None)
    try:
        dictionary = dictionary.replace(")", "")
        dictionary = dictionary.replace("'", '"')
        handle_dictionary(data, dictionary, request_id, requestor_id)
    except:
        pass


def handle_dictionary(data, dictionary, request_id, requestor_id):
    print("Received: " + str(dictionary))
    instance = transform_json_to_instance(dictionary)
    prediction = predict_instance(MODEL_PATH, instance)
    {"instance": data, "prediction": str(prediction)}
    for elem in str(prediction):
        if elem == "1":
            response = "System Violation"
            send_results.send_results(
                request_id, requestor_id, str(dictionary), response
            )
            return "System Violation"
        elif elem == "0":
            response = "Correct Invocation"
            send_results.send_results(
                request_id, requestor_id, str(dictionary), response
            )
            print("Correct Invocation")
            return "Correct Invocation"
