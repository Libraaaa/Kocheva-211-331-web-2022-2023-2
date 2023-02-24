# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

CAM_file = 'CAM_table.txt'
result = []
with open(CAM_file) as file:
    for line in file:
        list_table = line.split()
        if len(line.split('.')) == 3:
            vlan = list_table[0]
            mac = list_table[1]
            ports = list_table[3]
            result.append([int(vlan), mac, ports])

vlan_input = input('Enter VLAN number: ')
print(type(vlan_input))
for vlan, mac, ports in sorted(result):
    if int(vlan_input) == vlan:
        print('{:<10} {:<20} {:<15}'.format(vlan, mac, ports))