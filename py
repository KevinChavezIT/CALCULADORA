import http.client
import json
from datetime import datetime, timedelta, timezone
import ssl

#create unsecure https connection from IP and port
def get_connection(ip, port):
    try:
        connection = http.client.HTTPSConnection(ip, port, context=ssl._create_unverified_context())
        return connection
    except Exception as e:
        return "Not is possible to create http connection from {}, error {}".format(ip, e)


#Get token from alletra storage
def get_token(connection, username, password):
    url = '/v1/tokens'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "data": {
            "username": username,
            "password": password
        }
    }
    connection.request("POST", url, body=json.dumps(data), headers=headers)
    response = connection.getresponse()
    response_data = response.read().decode()
    connection.close()

    return json.loads(response_data)["data"]["session_token"]


#Get events from storage according to catedogy and severity
def get_events(connection, xtoken, category, severity):
    url = f'/v1/events/detail?category={category}&severity={severity}'
    headers = {
        'X-Auth-Token': xtoken
    }
    connection.request("GET", url, headers=headers)
    response = connection.getresponse()
    response_data = response.read().decode()
    connection.close()

    if response.status == 200:
        return json.loads(response_data)
    else:
        print(f'Error {response.status}: {response_data}')


#format events from eventlist in list format separated by ;
def format_events_from_json(event_list, hostname):
    now = datetime.now().astimezone()
    date_limit = now - timedelta(hours=1) #control events according to time in back from now
    event_list = []

    for event in events["data"]:
        if datetime.fromtimestamp(event["timestamp"]).astimezone() > date_limit:
            event_list.append("{};{};{};{};{};{};{}".format(hostname,  event["activity"],  event["category"],
                                                            event["severity"], event["target"], event["target_type"],
                                                            datetime.fromtimestamp(event["timestamp"]).strftime('%Y/%m/%d %H:%M:%S')
                                                            )
                              )

    return event_list

#only to test without date control, print all events
def format_events_from_json_to_test(event_list, hostname):
    now = datetime.now().astimezone()
    date_limit = now - timedelta(days=2)
    event_list = []

    for event in events["data"]:
        event_list.append("{};{};{};{};{};{};{}".format(hostname,  event["activity"],  event["category"],
                                                        event["severity"], event["target"], event["target_type"],
                                                        datetime.fromtimestamp(event["timestamp"]).strftime('%Y/%m/%d %H:%M:%S')
                                                        )
                            )

    return event_list


#Write events to log file, here dynatrace will read events
def write_events_to_file(filtered_logs):
    try:
        #event_file = open("/opt/IBM/LOGS/sansw_monitor.log", "a")
        if filtered_logs != "":
            event_file = open("/opt/IBM/LOGS/alletra_monitor.log", "a")
            for line in filtered_logs:
                event_file.write("{}\n".format(line))
            event_file.close()
    except Exception as e:
        event_file.write("Not is possible to write file due error: {}".format(e))

"""
Event category:
    Possible values: 'unknown', 'hardware', 'service', 'replication', 'volume', 'update', 'configuration', 'test', 'security'.
Event severity:
    Possible values: 'info', 'notice', 'warning', 'critical'.
"""
configuration = [
    ["10.151.41.60", "PRECSTG001", 5392, "operador", "30mYz2A", "hardware", "warning"],
    ["10.151.41.60", "PRECSTG001", 5392, "operador", "30mYz2A", "configuration", "warning"],
    ["10.151.41.60", "PRECSTG001", 5392, "operador", "30mYz2A", "volume", "warning"],
    ["10.151.41.60", "PRECSTG001", 5392, "operador", "30mYz2A", "hardware", "critical"],
    ["10.151.41.60", "PRECSTG001", 5392, "operador", "30mYz2A", "configuration", "critical"],
    ["10.151.41.60", "PRECSTG001", 5392, "operador", "30mYz2A", "volume", "critical"],
    ["10.151.41.129", "DRECSTG001", 5392, "operador", "30mYz2A", "hardware", "warning"],
    ["10.151.41.129", "DRECSTG001", 5392, "operador", "30mYz2A", "configuration", "warning"],
    ["10.151.41.129", "DRECSTG001", 5392, "operador", "30mYz2A", "volume", "critical"],
    ["10.151.41.129", "DRECSTG001", 5392, "operador", "30mYz2A", "hardware", "critical"],
    ["10.151.41.129", "DRECSTG001", 5392, "operador", "30mYz2A", "configuration", "critical"],
    ["10.151.41.129", "DRECSTG001", 5392, "operador", "30mYz2A", "volume", "critical"],

                  ]


for stg in configuration:
    connection = get_connection(stg[0], stg[2])
    token = get_token(connection, stg[3], stg[4])
    events = get_events(connection, token, stg[5], stg[6])
    event_list = format_events_from_json(events, stg[1])
    write_events_to_file(event_list)

