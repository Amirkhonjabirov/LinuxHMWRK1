from subprocess import run
import datetime

subprocss = run("ps aux", shell=True, capture_output=True).stdout.decode('utf-8').rstrip()
result = subprocss.split('\n')
processes = len(result) - 1
users_and_processes = {}
using_max_cpu = [result[1].split()[10][:20], 0]
using_max_mem = [result[1].split()[10][:20], 0]


def generate_log_file():
    cpu = 0
    memory = 0

    filename = f"{datetime.now().strftime('%d-%m-%Y_%H:%M')}_scan.txt"

    for i in result[1:]:
        row = i.split()
        cpu += float(row[2])
        memory += float(row[3])

        if row[0] in users_and_processes.keys():
            users_and_processes[row[0]] += 1
        else:
            users_and_processes[row[0]] = 1

        if float(row[2]) > using_max_cpu[1]:
            using_max_cpu[0], using_max_cpu[1] = row[10][:20], float(row[2])

        if float(row[3]) > using_max_mem[1]:
            using_max_mem[0], using_max_mem[1] = row[10][:20], float(row[3])

    with open(filename, 'a') as f:
        f.write("Отчёт о состоянии системы:")
        f.write(f"Пользователи системы: {', '.join(i for i in users_and_processes.keys())}")
        f.write(f"Процессов запущено: {processes}")
        f.write("Пользовательских процессов:")
        for key, value in users_and_processes.items():
            f.write(f"{key}: {value}")
        f.write(f"Всего памяти используется: {memory}%")
        f.write(f"Всего CPU используется: {cpu}%")
        f.write(f"Больше всего памяти использует: {using_max_mem[0]}")
        f.write(f"Больше всего CPU использует: {using_max_cpu[0]}")


if __name__ == '__main__':
    generate_log_file()
