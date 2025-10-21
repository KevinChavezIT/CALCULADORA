import http.client
import ssl
import base64
import json

from datetime import datetime, timedelta



def create_https_connection(host, port ):
    """
    This method will create a connection object tha you can use to interact with CSM Hosts
    """
    return http.client.HTTPSConnection(host, port, context = ssl._create_unverified_context())



def get_brocade_chassis_info(connection, hostname_IP, sansw_name, auth):
    try:
        headers = {
            'Accept': 'application/yang-data+json',
            'Authorization': f'Basic {auth}'
        }
        now = datetime.now().astimezone()  # Asegurarse de que 'now' tenga información de zona horaria
        date_limit = now - timedelta(hours=1) # Tiempo en el que obtiene la data

        connection.request("GET", "/rest/running/brocade-logging/error-log", headers=headers)
        response = connection.getresponse()
        if response.status == 200:  # Verificar que la solicitud fue exitosa (código de estado 200)
            data = response.read().decode()
            filtered_logs = []
            if data:  # Verificar si la respuesta contiene datos
                logs = json.loads(data)
            if data:  # Verificar si la respuesta contiene datos
                logs = json.loads(data)
                for log in logs["Response"]["error-log"]:
                    if log["severity-level"] in ["error", "warning", "critical"] and datetime.fromisoformat(log["time-stamp"]).astimezone() > date_limit:
                        filtered_logs.append("{};{};{};{};{};{}".format(sansw_name, log["time-stamp"], log["severity-level"], log["switch-user-friendly-name"], log["fabric-id"], log["message-text"]))
                connection.close()
                return filtered_logs
            else:
                print("La respuesta del servidor no contiene datos JSON.")
        else:
            print("La solicitud no fue exitosa. Código de estado: {}".format(response.status))
    except Exception as error:
        error_message = "No es posible conectar con el sansw {}. Error: {}".format(sansw_name, error)
        print(error_message)
        write_events_to_file(error_message)
        connection.close()


def write_events_to_file(filtered_logs):
    try:
        #event_file = open("/opt/IBM/LOGS/sansw_monitor.log", "a")
        if filtered_logs != "":
            event_file = open("C:/IBM/LOGS/sansw_monitor.log", "a")
            for line in filtered_logs:
                event_file.write("{}\n".format(line))
            event_file.close()
    except Exception as e:
        event_file.write("No se puede escribir el log debido al error: {}".format(e))


if __name__ == '__main__':
    username = 'monbrocade'
    password = 'monbrocade2025*'
    auth = base64.b64encode(f'{username}:{password}'.encode()).decode()
    list_of_hosts = ['10.70.89.82', 'sansw_bp53'], ['10.70.89.86', 'sansw_bp54'], ['10.70.89.85', 'sansw_bp61'], ['10.70.89.89', 'sansw_bp62'], ['172.26.8.96', 'sansw_bp153'], ['172.26.8.100', 'sansw_bp154'], ['172.26.8.99', 'sansw_bp161'], ['172.26.8.103', 'sansw_bp162'],
    #list_of_hosts = ['10.70.89.82', 'sansw_bp53'], ['10.70.89.86', 'sansw_bp54'], ['10.70.89.85', 'sansw_bp61'], ['10.70.89.89', 'sansw_bp62']
    for i in list_of_hosts:
        hostname_IP = '{}'.format(i[0])
        connection = create_https_connection(hostname_IP, 443)
        filtered_logs = get_brocade_chassis_info(connection, hostname_IP, i[1], auth)
        write_events_to_file(filtered_logs)

