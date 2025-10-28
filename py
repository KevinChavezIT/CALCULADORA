---
- name: Ejecutar script Python para login y consulta de LUNs
  hosts: localhost
  gather_facts: true
  vars:
    info_dir: "C:\\info_luns"
  tasks:

  pre_tasks:
    - name: Log start of playbook execution
      ansible.builtin.include_role:
        name: pichincha.sre.pre_task

    - name: Ejecutar script usando variables de entorno
      ansible.builtin.shell:
        cmd: python3 spectrum_login.py
        executable: /bin/bash
      environment:
        LOGIN_USER: "{{ LOGIN_USER }}"
        LOGIN_PASS: "{{ LOGIN_PASS }}"
      changed_when: false

    - name: Leer archivo JSON generado
      ansible.builtin.slurp:
        src: luns_response.json
      register: luns_json_raw

    - name: Decodificar contenido JSON
      ansible.builtin.set_fact:
        luns_data: "{{ luns_json_raw.content | b64decode | from_json }}"

    - name: Mostrar contenido de luns_data
      ansible.builtin.debug:
        var: luns_data[:10]

    - name: Filtrar LUNs con Hosts definidos y no vacíos
      ansible.builtin.set_fact:
        luns_filtrados: >-
          {{
            luns_data
            | selectattr('Hosts', 'defined')
            | rejectattr('Hosts', 'equalto', '')
            | list
          }}

    - name: Clasificar LUNs por Storage System
      ansible.builtin.set_fact:
        luns_por_equipo: >-
          {{
            {
              "Prod1": luns_filtrados | selectattr("Storage System", "equalto", "IBM.2107-75LGN01") | list,
              "prod2": luns_filtrados | selectattr("Storage System", "equalto", "IBM.2107-75LGW31") | list,
              "cont1": luns_filtrados | selectattr("Storage System", "equalto", "IBM.2107-75LGN21") | list,
              "7200": luns_filtrados | selectattr("Storage System", "equalto", "FS7200") | list
            }
          }}

    - name: Construir CSV para Prod1
      ansible.builtin.set_fact:
        csv_prod1: |
          Estado
          Mediciones Mensuales
          Total LUNs,Disponibilidad Esperada(min),Disponibilidad Real(%)
          {% set total_luns = (luns_por_equipo.Prod1 | length) | int %}
          {% set fecha_corte = ansible_date_time.date %}
          {% set dia_del_mes = fecha_corte.split('-')[2] | int %}
          {% set dise_min = (24 * 60 * dia_del_mes) | int %}
          {% set indis_min = 0 | int %}
          {% set disr_min = dise_min - indis_min %}
          {% set disponibilidad_esperada = (dise_min * total_luns) %}
          {% set disponibilidad_real = (((disr_min * total_luns) / disponibilidad_esperada) * 100) %}
          {{ total_luns }},{{ disponibilidad_esperada | int }},{{ disponibilidad_real | round(2) }}
          Name,HostGroups,Fecha Corte,Dia del Mes,DISE(min),INDIS(min),DISR(min)
          {% for lun in luns_por_equipo.Prod1 %}
          {{ lun.Name }},{{ lun.Hosts }},{{ fecha_corte }},{{ dia_del_mes }},{{ dise_min }},{{ indis_min }},{{ disr_min }}
          {% endfor %}

    - name: Construir CSV para prod2
      ansible.builtin.set_fact:
        csv_prod2: |
          Name,HostGroups,Fecha Corte,Dia del Mes,DISE(min),INDIS(min),DISR(min)
          {% set fecha_corte = ansible_date_time.date %}
          {% set dia_del_mes = fecha_corte.split('-')[2] | int %}
          {% set dise_min = 24 * 60 * dia_del_mes %}
          {% set indis_min = 0 %}
          {% set disr_min = dise_min - indis_min %}
          {% for lun in luns_por_equipo.prod2 %}
          {{ lun.Name }},{{ lun.Hosts }},{{ fecha_corte }},{{ dia_del_mes }},{{ dise_min }},{{ indis_min }},{{ disr_min }}
          {% endfor %}

    - name: Construir CSV para cont1
      ansible.builtin.set_fact:
        csv_cont1: |
          Name,HostGroups,Fecha Corte,Dia del Mes,DISE(min),INDIS(min),DISR(min)
          {% set fecha_corte = ansible_date_time.date %}
          {% set dia_del_mes = fecha_corte.split('-')[2] | int %}
          {% set dise_min = 24 * 60 * dia_del_mes %}
          {% set indis_min = 0 %}
          {% set disr_min = dise_min - indis_min %}
          {% for lun in luns_por_equipo.cont1 %}
          {{ lun.Name }},{{ lun.Hosts }},{{ fecha_corte }},{{ dia_del_mes }},{{ dise_min }},{{ indis_min }},{{ disr_min }}
          {% endfor %}

    - name: Construir CSV para 7200
      ansible.builtin.set_fact:
        csv_7200: |
          Name,HostGroups,Fecha Corte,Dia del Mes,DISE(min),INDIS(min),DISR(min)
          {% set fecha_corte = ansible_date_time.date %}
          {% set dia_del_mes = fecha_corte.split('-')[2] | int %}
          {% set dise_min = 24 * 60 * dia_del_mes %}
          {% set indis_min = 0 %}
          {% set disr_min = dise_min - indis_min %}
          {% for lun in luns_por_equipo['7200'] %}
          {{ lun.Name }},{{ lun.Hosts }},{{ fecha_corte }},{{ dia_del_mes }},{{ dise_min }},{{ indis_min }},{{ disr_min }}
          {% endfor %}

    - name: Guardar CSV Prod1
      ansible.builtin.copy:
        content: "{{ csv_prod1 }}"
        dest: "{{ info_dir }}\\luns_Prod1.csv"
        mode: '0644'
        force: true

    - name: Guardar CSV prod2
      ansible.builtin.copy:
        content: "{{ csv_prod2 }}"
        dest: "{{ info_dir }}\\luns_prod2.csv"
        mode: '0644'
        force: true

    - name: Guardar CSV cont1
      ansible.builtin.copy:
        content: "{{ csv_cont1 }}"
        dest: "{{ info_dir }}\\luns_cont1.csv"
        mode: '0644'
        force: true

    - name: Guardar CSV 7200
      ansible.builtin.copy:
        content: "{{ csv_7200 }}"
        dest: "{{ info_dir }}\\luns_7200.csv"
        mode: '0644'
        force: true

  post_tasks:
    - name: Log end of playbook execution
      ansible.builtin.include_role:
        name: pichincha.sre.post_task


- name: Copiar CSV al servidor Windows destino
  hosts: server_guardar_info
  gather_facts: false
  vars:
    info_dir: "C:\\info_luns"
  tasks:

  pre_tasks:
    - name: Log start of playbook execution
      ansible.builtin.include_role:
        name: pichincha.sre.pre_task

    - name: Obtener timestamp desde PowerShell
      ansible.windows.win_shell: |
        Get-Date -Format "yyyy-MM-dd_HHmmss"
      register: timestamp_result

    - name: Definir timestamp como variable
      ansible.builtin.set_fact:
        timestamp: "{{ timestamp_result.stdout | trim }}"

    - name: Definir nombre de archivo con timestamp
      ansible.builtin.set_fact:
        csv_prod1: "luns_Prod1_{{ timestamp }}.csv"
        csv_prod2: "luns_prod2_{{ timestamp }}.csv"
        csv_cont1: "luns_cont1_{{ timestamp }}.csv"
        csv_7200: "luns_7200_{{ timestamp }}.csv"

    - name: Copiar CSV Prod1
      ansible.windows.win_copy:
        src: "C:\\info_luns\\luns_Prod1.csv"
        dest: "{{ info_dir }}\\{{ csv_prod1 }}"

    - name: Copiar CSV prod2
      ansible.windows.win_copy:
        src: "C:\\info_luns\\luns_prod2.csv"
        dest: "{{ info_dir }}\\{{ csv_prod2 }}"

    - name: Copiar CSV cont1
      ansible.windows.win_copy:
        src: "C:\\info_luns\\luns_cont1.csv"
        dest: "{{ info_dir }}\\{{ csv_cont1 }}"

    - name: Copiar CSV 7200
      ansible.windows.win_copy:
        src: "C:\\info_luns\\luns_7200.csv"
        dest: "{{ info_dir }}\\{{ csv_7200 }}"

  post_tasks:
    - name: Log end of playbook execution
      ansible.builtin.include_role:
        name: pichincha.sre.post_task
