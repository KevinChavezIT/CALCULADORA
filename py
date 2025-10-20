import http.client
import ssl
import json
from datetime import datetime
from urllib.parse import urlencode
from os import  getcwd

# ... (las otras funciones igual)

def get_sessions_summary(connection, token):
    """
    This method returns the overview summary information for all sessions managed by the server
    """
    try:
        headers = {"X-Auth-Token":"{}".format(token)}
        baseurl="/CSM/web/sessions/short"

        connection.request("GET", baseurl, headers=headers)
        response = connection.getresponse()

        print(f"DEBUG: Status code de sesiones: {response.status}")  # <-- AGREGAR ESTA LINEA
        
        if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
            data = response.read().decode()
            if data:  # Verificar si la respuesta contiene datos
                json_response = json.loads(data)
                print(f"DEBUG: Se obtuvieron {len(json_response)} sesiones")  # <-- AGREGAR ESTA LINEA
                return [{"name": item["name"], "status": item["status"], "state": item["state"]} for item in json_response]
            else:
                print("La respuesta del servidor no contiene datos JSON.")
        else:
            print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))

    except Exception as error:
        print("an error was raised see deatils: {} ".format(error))
        connection.close()


def get_session_error_state(session_summary):
    list_of_sessions = []
    print(f"DEBUG: Analizando {len(session_summary)} sesiones")  # <-- AGREGAR ESTA LINEA
    for i in session_summary:
        if i['state'] == 'Prepared' or i['state'] == 'Defined' or i['state'] == 'Protected':
            pass
        else:
            list_of_sessions.append({"name": i["name"], "state": i["state"]})
    
    print(f"DEBUG: Sesiones anormales encontradas: {len(list_of_sessions)}")  # <-- AGREGAR ESTA LINEA
    return list_of_sessions


def write_events_to_file(format_time, alert_type, alerted_host, events_list):
    print(f"DEBUG: Escribiendo en log - Tipo: {type(events_list)}, Longitud: {len(events_list) if isinstance(events_list, list) else 'N/A'}")  # <-- AGREGAR ESTA LINEA
    
    if type(events_list) is list:
        event_file = open("C:/IBM/LOGS/SpectrumControlLOG.log", "a")  # append mode
        if len(events_list) > 0:
            for i in events_list:
                event_file.write("{};{};{};session name: {} are in anormal state: {}, plase check\n".format(format_time, alert_type, alerted_host, i["name"], i["state"]))
            print(f"DEBUG: Escritas {len(events_list)} entradas en log")  # <-- AGREGAR ESTA LINEA
        else:
            event_file.write("{};{};{};No abnormal sessions found\n".format(format_time, alert_type, alerted_host))
            print("DEBUG: Escrito 'No abnormal sessions found' en log")  # <-- AGREGAR ESTA LINEA
        event_file.close()

    else:
        event_file = open("C:/IBM/LOGS/SpectrumControlLOG.log", "a")  # append mode
        event_file.write("{};{};{};{}\n".format(format_time, alert_type, alerted_host, events_list))
        event_file.close()
        print(f"DEBUG: Escrito evento simple en log: {events_list}")  # <-- AGREGAR ESTA LINEA




if __name__ == '__main__':
    print("=== INICIANDO SCRIPT CSM ===")  # <-- AGREGAR ESTA LINEA
    hostname_IP = '10.70.152.131'

    connection = create_https_connection(hostname_IP)
    token = get_token_from_csm(connection, 'operador', 'hgpANwHPk5q}g.Y', hostname_IP)

    if token:
        print("DEBUG: Token obtenido exitosamente")  # <-- AGREGAR ESTA LINEA
        events_list = get_session_error_state(get_sessions_summary(connection, token))
        write_events_to_file(get_date_time("%d-%m-%Y-%H:%M:%S"), "CSM event", "Copy Services Manager", events_list)
    else:
        print("DEBUG: Error - No se pudo obtener token")  # <-- AGREGAR ESTA LINEA

    print("=== SCRIPT FINALIZADO ===")  # <-- AGREGAR ESTA LINEA
