#Teste 1 de GPU
# import igpu

# gpu_count = igpu.count_devices()
# gpu = igpu.get_device(0)
# print(f'This host has {gpu_count} devices.')
# print(f'The first gpu is a {gpu.name} with {gpu.memory.total:.0f}{gpu.memory.unit}.')



#Teste 2 de GPU
# _GPU = False
# _NUMBER_OF_GPU = 0

# def _check_gpu():
#     global _GPU
#     global _NUMBER_OF_GPU
#     nvidia_smi.nvmlInit()
#     _NUMBER_OF_GPU = nvidia_smi.nvmlDeviceGetCount()
#     if _NUMBER_OF_GPU > 0:
#         _GPU = True

# def _print_gpu_usage(detailed=False):

#     if not detailed:
#         for i in range(_NUMBER_OF_GPU):
#             handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
#             info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
#             print(f'GPU-{i}: GPU-Memory: {_bytes_to_megabytes(info.used)}/{_bytes_to_megabytes(info.total)} MB')

# def _bytes_to_megabytes(bytes):
#     return round((bytes/1024)/1024,2)

# if __name__ == '__main__':
#     print('Checking for Nvidia GPU\n')
#     _check_gpu()
#     if _GPU:
#         _print_gpu_usage()
#     else:
#         print("No GPU found.")

import psutil
import subprocess

battery = psutil.sensors_battery()
users = psutil.users()
temperatures = psutil.sensors_temperatures()
#print(temperatures.nvme)

def get_user_name():
    return users[0].name

def get_user_pid():
    return users[0].pid #pid do processo de login


def secs2hours(secs):
    if battery == None:
        return ""
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

def get_battery_percent():
    if battery == None:
        return ""
    return battery.percent

def get_battery_time_left():
    if battery == None:
        return ""
    return secs2hours(battery.secsleft)

def get_battery_plugged():
    if battery == None:
        return ""
    return battery.power_plugged

def get_motherboard():
    command_data = subprocess.run(
        "sudo dmidecode -t 2 | grep Product", shell=True, capture_output=True).stdout.decode().strip()

    return command_data.replace("Product Name:", "")

def get_gpu():
    command_data = subprocess.run(
        "lshw -numeric -C display | grep product | head -n 1", shell=True, capture_output=True).stdout.decode().strip()

    command_data = command_data.split('[')
    #command_data = command_data.replace('product:', '')
    
    return command_data[1].replace(']','')

