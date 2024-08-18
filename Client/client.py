import psutil
import platform
import subprocess
from datetime import datetime
import cpuinfo
import socket
import uuid
import re
import humanize
import requests
import json

def Hardware_information():
    
    # System Info
    sysinfo = {
        'system' : platform.system(),
        'node' : platform.node(),
        'relase' : platform.release(),
        'version' : platform.version(),
        'machine' : platform.machine(),
        'processor' : cpuinfo.get_cpu_info()['brand_raw'],
        'ip_address' : socket.gethostbyname(socket.gethostname()),
        'mac_address' : ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    }


    # Boot Time
    boot = psutil.boot_time()
    sysinfo['boot_time'] = datetime.utcfromtimestamp(boot).strftime('%Y-%m-%d %H:%M:%S') 

    # CPU info
    cpu = {

        # Number of cores
        'physical_cores' : psutil.cpu_count(),
        'total_cores' : psutil.cpu_count(logical=False),

        # CPU frequencies
        'max_frequency' : psutil.cpu_freq().max,
        'min_frequency' : psutil.cpu_freq().min,
        'current_frequency' : psutil.cpu_freq().current
    }

    # CPU usage
    cpu['core_usage'] = []
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        core = {
            'number': i,
            'usage': percentage
        }
        cpu['core_usage'].append(core)
    cpu['total_cpu_usage'] = psutil.cpu_percent()

    # Memory Information
    memory = {
        'total' : humanize.naturalsize(psutil.virtual_memory().total),
        'available' : humanize.naturalsize(psutil.virtual_memory().available),
        'used' : humanize.naturalsize(psutil.virtual_memory().used),
        'percentage' : psutil.virtual_memory().percent
        
    }
    # Swap information
    swap = {
        "total" : humanize.naturalsize(psutil.swap_memory().total),
        "free" : humanize.naturalsize(psutil.swap_memory().free),
        "used" : humanize.naturalsize(psutil.swap_memory().used),
        "percentage" : psutil.swap_memory().percent
    }

    # Disk Information

    disks = []

    for partition in psutil.disk_partitions():

        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        
        disk = {
        'device' : partition.device,
        'mountpoint' : partition.mountpoint,
        'fstype' : partition.fstype,
        'total_size' : humanize.naturalsize(partition_usage.total),
        'used' : humanize.naturalsize(partition_usage.used),
        'free' : humanize.naturalsize(partition_usage.free),
        'percentage' : partition_usage.percent
        }
        disks.append(disk)

    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    iostats = {
        'disk_read': humanize.naturalsize(disk_io.read_bytes),
        'disk_write': humanize.naturalsize(disk_io.write_bytes),
        'network_sent': humanize.naturalsize(net_io.bytes_sent),
        'network_received': humanize.naturalsize(net_io.bytes_recv)
    }

   # get info about running processes
    proceses = []

    for process in psutil.process_iter():
        process = psutil.Process(process.pid)
        start_time = datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        process_info = {
            "pid": process.pid,
            "name": process.name(),
            "start_time": start_time,
            "cpu_usage": process.cpu_percent()
        }
        
        proceses.append(process_info)

    list_of_apps = []
    if sysinfo['system'] == 'Linux':
        cmd = ["pacman", "-Qe"]
        installed_apps = subprocess.check_output(cmd).decode("latin-1").split("\n")
        
        for app in installed_apps:
            app = app.strip()
            list_of_apps.append(app)
        
    elif sysinfo['system'] == 'Windows':
        cmd = ["powershell.exe", "Get-ItemProperty", "HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*", "|", "Select-Object", "DisplayName"]
        installed_apps = subprocess.check_output(cmd).decode("latin-1").split("\n")
       

        for app in installed_apps[3:]:
            app = app.strip()
            if app: list_of_apps.append(app)
        


    return {'processes':proceses, 
            "list_of_apps":list_of_apps,
            "sysinfo":sysinfo,
            "cpu":cpu,
            "memory":memory,
            "swap":swap,
            "disks":disks,
            "iostats":iostats
            }
            
if __name__ == "__main__":


    while(True):
        info = Hardware_information()
        json_data = json.dumps(info)
        headers = {'Content-type': 'application/json'}
        response = requests.post("http://localhost:8000/recive_data/", data=json_data, headers=headers)
        print(response)