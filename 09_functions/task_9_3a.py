# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    access_dictionary = {}
    trunk_dictionary = {}
    interface = ''
    with open(config_filename) as config_file:
        for line in config_file:
            if line.startswith('interface'):
                interface = line.split()[-1]
            if line != '!' and interface != '':
                if line.find('access vlan') != -1:
                    access_dictionary[interface] = int(line.split()[-1])
                elif line.find('mode access') != -1:
                    access_dictionary[interface] = 1
                elif line.find('trunk allowed') != -1:
                    vlans_trunk = line.split()[-1].split(',')
                    trunk_dictionary[interface] = list(map(int, vlans_trunk))
            else: interface = ''
    return access_dictionary, trunk_dictionary

print(get_int_vlan_map('config_sw2.txt'))