- name: Contar LUNs únicos por Name para Prod1
  ansible.builtin.set_fact:
    total_luns_prod1: "{{ luns_por_equipo.Prod1 | selectattr('Name', 'defined') | selectattr('Name', 'ne', '') | map(attribute='Name') | unique | list | length }}"

- name: Debug - Mostrar conteo real
  ansible.builtin.debug:
    msg: "Total LUNs Prod1 (por Name): {{ total_luns_prod1 }}"

- name: Construir CSV para Prod1
  ansible.builtin.set_fact:
    csv_prod1: |
      Estado
      Mediciones Mensuales
      Total LUNs,Disponibilidad Esperada(min),Disponibilidad Real(%)
      {% set total_luns = total_luns_prod1 | int %}
      {% set fecha_corte = ansible_date_time.date %}
      {% set dia_del_mes = fecha_corte.split('-')[2] | int %}
      {% set dise_min = (24 * 60 * dia_del_mes) | int %}
      {% set indis_min = 0 | int %}
      {% set disr_min = dise_min - indis_min %}
      {% set disponibilidad_esperada = (dise_min * total_luns) | int %}
      {% set disponibilidad_real = (((disr_min * total_luns) / disponibilidad_esperada) * 100) if disponibilidad_esperada > 0 else 100 %}
      {{ total_luns }},{{ disponibilidad_esperada }},{{ disponibilidad_real | round(2) }}
      Name,HostGroups,Fecha Corte,Dia del Mes,DISE(min),INDIS(min),DISR(min)
      {% for lun in luns_por_equipo.Prod1 %}
      {{ lun.Name }},{{ lun.Hosts }},{{ fecha_corte }},{{ dia_del_mes }},{{ dise_min }},{{ indis_min }},{{ disr_min }}
      {% endfor %}