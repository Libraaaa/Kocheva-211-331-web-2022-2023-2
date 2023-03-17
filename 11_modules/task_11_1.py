# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент
вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое
файла в строку, а затем передать строку как аргумент функции (как передать вывод
команды показано в коде ниже).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

В словаре интерфейсы должны быть записаны без пробела между типом и именем.
То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt. При этом функция должна
работать и на других файлах (тест проверяет работу функции на выводе
из sh_cdp_n_sw1.txt и sh_cdp_n_r3.txt).

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def parse_cdp_neighbors(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
    получен вывод команды с оборудования. Принимая как аргумент вывод команды,
    вместо имени файла, мы делаем функцию более универсальной: она может работать
    и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """
    command = command_output.split('\n')
    main_device = ''
    neighbors = {}
    for line in command:
        if line != '':
            if main_device == '':
                main_device = line[:line.find('>')]
                continue
            if line.startswith('R') or line.startswith('SW'):
                subline = line.split()
                local_interface = subline[1] + subline[2]
                port_id = subline[-2] + subline[-1]
                neighbor = subline[0]
                neighbors[(main_device, local_interface)] = (neighbor, port_id)
    return neighbors

        
if __name__ == "__main__":
    print('SW1')
    with open("D:/web/11_modules/sh_cdp_n_sw1.txt") as f:
        dictionary_neighbors = parse_cdp_neighbors(f.read())
        for key, value in dictionary_neighbors.items():
            print(key, ':', value) 
    # print('\nR3')
    # with open("D:/web/11_modules/sh_cdp_n_r3.txt") as f:
    #     dictionary_neighbors = parse_cdp_neighbors(f.read())
    #     for key, value in dictionary_neighbors.items():
    #         print(key, ':', value)