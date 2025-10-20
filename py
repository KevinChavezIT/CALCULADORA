py -c "
debug_script = '''import http.client
import ssl
import json
from datetime import datetime
from os import getcwd

def get_date_time(format_time):
    now = datetime.now()
    return now.strftime(format_time)

def create_https_connection(host):
    print(f'[DEBUG] Creando conexión a: {host}')
    return http.client.HTTPSConnection(host, context=ssl._create_unverified_context())

def get_token_from_csm(connection, username, password, host):
    try:
        print(f'[DEBUG] Intentando autenticación con usuario: {username}')
        headers = {
            'Accept-Language': 'en-US',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = f'username={username}&password={password}'
        connection.request('POST', '/CSM/web/system/v1/tokens', payload, headers)
        response = connection.getresponse()
        print(f'[DEBUG] Respuesta del servidor: {response.status}')
        
        if response.status == 200:
            data = response.read().decode()
            json_token_response = json.loads(data)
            token = json_token_response.get('token')
            if token:
                print(f'[DEBUG] ✓ Token obtenido exitosamente')
                return token
            else:
                print('[DEBUG] ✗ No se encontró token en la respuesta')
                return None
        else:
            print(f'[DEBUG] ✗ Error HTTP: {response.status}')
            return None
            
    except Exception as error:
        print(f'[DEBUG] ✗ Excepción en autenticación: {error}')
        return None

def get_sessions_summary(connection, token):
    try:
        print('[DEBUG] Obteniendo resumen de sesiones...')
        headers = {'X-Auth-Token': token}
        connection.request('GET', '/CSM/web/sessions/short', headers=headers)
        response = connection.getresponse()
        print(f'[DEBUG] Respuesta sesiones: {response.status}')
        
        if response.status == 200:
            data = response.read().decode()
            if data:
                json_response = json.loads(data)
                print(f'[DEBUG] ✓ Se obtuvieron {len(json_response)} sesiones')
                return [{'name': item['name'], 'status': item['status'], 'state': item['state']} for item in json_response]
            else:
                print('[DEBUG] ✗ Respuesta vacía')
                return []
        else:
            print(f'[DEBUG] ✗ Error obteniendo sesiones: {response.status}')
            return []
            
    except Exception as error:
        print(f'[DEBUG] ✗ Error en get_sessions_summary: {error}')
        return []

def get_session_error_state(session_summary):
    print(f'[DEBUG] Analizando {len(session_summary)} sesiones...')
    list_of_sessions = []
    for i in session_summary:
        if i['state'] in ['Prepared', 'Defined', 'Protected']:
            continue
        else:
            list_of_sessions.append({'name': i['name'], 'state': i['state']})
    
    print(f'[DEBUG] ✓ Sesiones anormales encontradas: {len(list_of_sessions)}')
    return list_of_sessions

def write_events_to_file(format_time, alert_type, alerted_host, events_list):
    log_path = 'C:/IBM/LOGS/SpectrumControlLOG.log'
    try:
        print(f'[DEBUG] Escribiendo en log: {log_path}')
        
        if type(events_list) is list:
            with open(log_path, 'a', encoding='utf-8') as event_file:
                if len(events_list) > 0:
                    for i in events_list:
                        line = f'{format_time};{alert_type};{alerted_host};session name: {i[\"name\"]} are in abnormal state: {i[\"state\"]}, please check\\n'
                        event_file.write(line)
                        print(f'[DEBUG] ✓ Escrito en log: {i[\"name\"]} - {i[\"state\"]}')
                    print(f'[DEBUG] ✓ Total escritas {len(events_list)} entradas en log')
                else:
                    event_file.write(f'{format_time};{alert_type};{alerted_host};No abnormal sessions found\\n')
                    print('[DEBUG] ✓ Escrito: No abnormal sessions found')
        else:
            with open(log_path, 'a', encoding='utf-8') as event_file:
                event_file.write(f'{format_time};{alert_type};{alerted_host};{events_list}\\n')
                print(f'[DEBUG] ✓ Escrito evento simple: {events_list}')
                
    except Exception as e:
        print(f'[DEBUG] ✗ Error escribiendo en log: {e}')

if __name__ == '__main__':
    print('=== INICIANDO SCRIPT CSM MONITOR ===')
    hostname_IP = '10.70.152.131'
    
    connection = create_https_connection(hostname_IP)
    token = get_token_from_csm(connection, 'operador', 'hgpANwHPk5q}g.Y', hostname_IP)
    
    if token:
        print('[DEBUG] ✓ Token válido, procediendo a obtener sesiones...')
        sessions = get_sessions_summary(connection, token)
        if sessions:
            events_list = get_session_error_state(sessions)
            write_events_to_file(get_date_time('%d-%m-%Y-%H:%M:%S'), 'CSM event', 'Copy Services Manager', events_list)
        else:
            print('[DEBUG] ✗ No se pudieron obtener sesiones')
            write_events_to_file(get_date_time('%d-%m-%Y-%H:%M:%S'), 'CSM event', 'Copy Services Manager', 'No sessions retrieved')
    else:
        print('[DEBUG] ✗ No se pudo obtener token, escribiendo error en log...')
        write_events_to_file(get_date_time('%d-%m-%Y-%H:%M:%S'), 'CSM event', 'Copy Services Manager', 'Authentication failed')
    
    print('=== SCRIPT FINALIZADO ===')
'''

with open('C:/IBM/csm_mon_debug.py', 'w', encoding='utf-8') as f:
    f.write(debug_script)

print('✓ Script de debug creado: C:/IBM/csm_mon_debug.py')
print('✓ Ejecuta: python C:/IBM/csm_mon_debug.py')
"
