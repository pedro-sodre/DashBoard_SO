import psutil
import subprocess

battery = psutil.sensors_battery()
users = psutil.users()
temperatures = psutil.sensors_temperatures()

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
    command_data = command_data[0].split('product:')
    
    return command_data[1] #.replace(']','')

