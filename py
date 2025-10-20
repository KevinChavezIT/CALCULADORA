import http.client
import ssl
import json
from datetime import datetime
from urllib.parse import urlencode
from os import  getcwd
#import pandas as pd


def get_date_time(format_time):
    now = datetime.now()
    date_formated = now.strftime(format_time)
    return str(date_formated)


def create_https_connection(host):
    """
    This method will create a connection object tha you can use to interact with CSM Hosts
    """
    return http.client.HTTPSConnection(host, context = ssl._create_unverified_context())


def get_token_from_csm(connection, username, password, host):
    """
    This method will return a token needed to interact with CSM API-REST methods
    """
    try:
        headers = {
                    'Accept-Language': 'en-US',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

        payload = 'username={}&password={}'.format(username, password)

        # Realizar la solicitud POST
        connection.request("POST", "/CSM/web/system/v1/tokens", payload, headers)
        response = connection.getresponse()

        # get json string
        json_token_response = json.loads(response.read().decode())
        connection.close()

        return json_token_response['token']

    except Exception as error:
        error = "there is not possible to connect on CSM server {} error: {} ".format(hostname_IP, error)
        write_events_to_file(get_date_time("%d-%m-%Y-%H:%M:%S"), "Storage System", "Copy Services Manager", error)
        connection.close()


def get_paths_report(connection, token, stg_type):
    """
    Query for all the logical paths on the storage system
    """
    try:
        headers = {"X-Auth-Token":"{}".format(token)}
        baseurl="/CSM/web/storagedevices/paths"

        connection.request("GET", baseurl, headers=headers)
        response = connection.getresponse()

        if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
            data = response.read().decode()
            if data:  # Verificar si la respuesta contiene datos
                json_response = json.loads(data)
                return json_response
            else:
                print("La respuesta del servidor no contiene datos JSON.")
        else:
            print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))

    except Exception as error:
        print("an error was raised see deatils: {} ".format(error))
        connection.close()


def get_ports_not_in_redundance(port_list):
    """
    build a report with paths that nor are in higth redundance
    """
    pass


def get_all_volumes_by_storage(connection, storage_id, token):
    """
    This method will return all volumes for a given storage system based off the input devicename from the get storage devices query
    """
    try:
        headers = {"X-Auth-Token":"{}".format(token)}
        baseurl="/CSM/web/storagedevices/volumes/{}".format(storage_id)

        connection.request("GET", baseurl, headers=headers)
        response = connection.getresponse()

        if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
            data = response.read().decode()
            if data:  # Verificar si la respuesta contiene datos
                json_response = json.loads(data)
                return [{"ID": item["elementid"][-4:], "sessions": item["sessions"]} for item in json_response]
            else:
                print("La respuesta del servidor no contiene datos JSON.")
        else:
            print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))

    except Exception as error:
        print("an error was raised see deatils: {} ".format(error))
        connection.close()


def all_volumes_with_Sessions_in_df(list_of_volumes):
     df = pd.DataFrame(list_of_volumes)
     return df


def get_all_sessions_by_storage(connection, storage_id, token):
    """
    Gets all the session names containing copy sets with volumes on the given storage system.
    """
    try:
        headers = {"X-Auth-Token":"{}".format(token)}
        baseurl="/CSM/web/storagedevices/DS8000:BOX:2107.{}/sessions".format(storage_id)

        connection.request("GET", baseurl, headers=headers)
        response = connection.getresponse()

        if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
            data = response.read().decode()
            if data:  # Verificar si la respuesta contiene datos
                json_response = json.loads(data)
                return json_response
            else:
                print("La respuesta del servidor no contiene datos JSON.")
        else:
            print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))

    except Exception as error:
        print("an error was raised see deatils: {} ".format(error))
        connection.close()


 #formatted_json = json.dumps(json_response, indent=2)  # Agregar indentación de 2 espacios


def get_sessions_summary(connection, token):
    """
    This method returns the overview summary information for all sessions managed by the server
    """
    try:
        headers = {"X-Auth-Token":"{}".format(token)}
        baseurl="/CSM/web/sessions/short"

        connection.request("GET", baseurl, headers=headers)
        response = connection.getresponse()

        print(f"DEBUG: Status code de sesiones: {response.status}")  # <-- DIAGNOSTICO
        
        if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
            data = response.read().decode()
            if data:  # Verificar si la respuesta contiene datos
                json_response = json.loads(data)
                print(f"DEBUG: Se obtuvieron {len(json_response)} sesiones")  # <-- DIAGNOSTICO
                return [{"name": item["name"], "status": item["status"], "state": item["state"]} for item in json_response]
            else:
                print("La respuesta del servidor no contiene datos JSON.")
        else:
            print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))

    except Exception as error:
        print("an error was raised see deatils: {} ".format(error))
        connection.close()


def get_session_in_normal_state(session_summary):
    list_of_sessions = []
    for i in session_summary:
        if i['status'] == 'Normal':
            list_of_sessions.append(i['name'])

    return list_of_sessions


def get_session_error_state(session_summary):
    list_of_sessions = []
    print(f"DEBUG: Analizando {len(session_summary)} sesiones")  # <-- DIAGNOSTICO
    for i in session_summary:
        if i['state'] == 'Prepared' or i['state'] == 'Defined' or i['state'] == 'Protected':
            pass
        else:
            list_of_sessions.append({"name": i["name"], "state": i["state"]})
    
    print(f"DEBUG: Sesiones anormales encontradas: {len(list_of_sessions)}")  # <-- DIAGNOSTICO
    return list_of_sessions


def download_sessions_in_csv(connection, token, list_of_sessions):
    """
    This method get all copysets for a session and export them to a csv file.
    """
    try:
        headers = {"X-Auth-Token":"{}".format(token)}
        for i in list_of_sessions:
            my_file = "{}\\reports\\{}.csv".format(getcwd(),i)

            baseurl="/CSM/web/sessions/{}/copysets/download".format(i)
            connection.request("GET", baseurl, headers=headers)
            response = connection.getresponse()

            if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
                with open(my_file, 'wb') as output_file:
                    chunk = response.read(128)
                    while chunk:
                        output_file.write(chunk)
                        chunk = response.read(128)
                print("Descarga exitosa. Archivo guardado en:", my_file)
            else:
                print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))

    except Exception as error:
        print("an error was raised see deatils: {} ".format(error))
        connection.close()


def write_events_to_file(format_time, alert_type, alerted_host, events_list):
    print(f"DEBUG: Escribiendo en log - Tipo: {type(events_list)}, Longitud: {len(events_list) if isinstance(events_list, list) else 'N/A'}")  # <-- DIAGNOSTICO
    
    if type(events_list) is list:
        event_file = open("C:/IBM/LOGS/SpectrumControlLOG.log", "a")  # append mode
        if len(events_list) > 0:
            for i in events_list:
                event_file.write("{};{};{};session name: {} are in anormal state: {}, plase check\n".format(format_time, alert_type, alerted_host, i["name"], i["state"]))
            print(f"DEBUG: Escritas {len(events_list)} entradas en log")  # <-- DIAGNOSTICO
        else:
            event_file.write("{};{};{};No abnormal sessions found\n".format(format_time, alert_type, alerted_host))
            print("DEBUG: Escrito 'No abnormal sessions found' en log")  # <-- DIAGNOSTICO
        event_file.close()

    else:
        event_file = open("C:/IBM/LOGS/SpectrumControlLOG.log", "a")  # append mode
        event_file.write("{};{};{};{}\n".format(format_time, alert_type, alerted_host, events_list))
        event_file.close()
        print(f"DEBUG: Escrito evento simple en log: {events_list}")  # <-- DIAGNOSTICO




if __name__ == '__main__':
    print("=== INICIANDO SCRIPT CSM ===")  # <-- DIAGNOSTICO
    hostname_IP = '10.70.152.131'

    connection = create_https_connection(hostname_IP)
    token = get_token_from_csm(connection, 'operador', 'hgpANwHPk5q}g.Y', hostname_IP)

    if token:
        print("DEBUG: Token obtenido exitosamente")  # <-- DIAGNOSTICO
        events_list = get_session_error_state(get_sessions_summary(connection, token))
        write_events_to_file(get_date_time("%d-%m-%Y-%H:%M:%S"), "CSM event", "Copy Services Manager", events_list)
    else:
        print("DEBUG: Error - No se pudo obtener token")  # <-- DIAGNOSTICO

    print("=== SCRIPT FINALIZADO ===")  # <-- DIAGNOSTICO
