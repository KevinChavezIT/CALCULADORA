- name: Calcular todas las métricas para Prod1
  ansible.builtin.set_fact:
    metrics_prod1:
      total_luns: "{{ total_luns_prod1 }}"
      fecha_corte: "{{ ansible_date_time.date }}"
      dia_del_mes: "{{ ansible_date_time.date.split('-')[2] | int }}"
      dise_min: "{{ (24 * 60 * ansible_date_time.date.split('-')[2] | int) | int }}"
      indis_min: 0
      disr_min: "{{ (24 * 60 * ansible_date_time.date.split('-')[2] | int) | int }}"
      disponibilidad_esperada: "{{ (24 * 60 * ansible_date_time.date.split('-')[2] | int * total_luns_prod1) | int }}"
      disponibilidad_real: 100.0

- name: Construir CSV para Prod1 (versión simplificada)
  ansible.builtin.set_fact:
    csv_prod1: |
      Estado
      Mediciones Mensuales
      Total LUNs,Disponibilidad Esperada(min),Disponibilidad Real(%)
      {{ metrics_prod1.total_luns }},{{ metrics_prod1.disponibilidad_esperada }},{{ metrics_prod1.disponibilidad_real }}
      Name,HostGroups,Fecha Corte,Dia del Mes,DISE(min),INDIS(min),DISR(min)
      {% for lun in luns_por_equipo.Prod1 %}
      {{ lun.Name }},{{ lun.Hosts }},{{ metrics_prod1.fecha_corte }},{{ metrics_prod1.dia_del_mes }},{{ metrics_prod1.dise_min }},{{ metrics_prod1.indis_min }},{{ metrics_prod1.disr_min }}
      {% endfor %}