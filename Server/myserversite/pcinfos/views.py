from django.shortcuts import render
from django.http import HttpResponse
from .models import Info, Process, Disk, Cpu_Cores, App
import json
import datetime

# render main website
def index(request):
    infos = Info.objects.all()
    return render(request, 'pcinfos/index.html', {'infos': infos})

# render website for certain pc
def pc(request, mac_address):
    try:
        pc = Info.objects.get(mac_address=mac_address)
    except Info.DoesNotExist:
        raise HttpResponse("error 404")
    return render(request,"pcinfos/pc.html", {'pc':pc})

# get data through POST request
def receive_data(request):
    if request.method == 'POST':

        # convert json data
        json_data = json.loads(request.body)
        sysinfo = json_data['sysinfo']
        cpu = json_data['cpu']
        memory = json_data['memory']
        swap = json_data['swap']
        disks = json_data['disks']
        iostats = json_data['iostats']

        # create new record or get existing one with same mac address
        obj, created = Info.objects.get_or_create(mac_address=sysinfo["mac_address"])

        # save systeminfo
        obj.system = sysinfo["system"]
        obj.node = sysinfo["node"]
        obj.relase = sysinfo["relase"]
        obj.version = sysinfo["version"]
        obj.machine = sysinfo["machine"]
        obj.processor = sysinfo["processor"]
        obj.ip_address = sysinfo["ip_address"]
        obj.mac_address = sysinfo["mac_address"]
        obj.boot_time = sysinfo["boot_time"]

        # save cpu info
        obj.physical_cores = cpu["physical_cores"]
        obj.total_cores =cpu["total_cores"]
        obj.max_frequency = cpu["max_frequency"]
        obj.min_frequency = cpu["min_frequency"]
        obj.current_frequency = cpu["current_frequency"]
        obj.core_usage = cpu["core_usage"]
        obj.total_cpu_usage = cpu["total_cpu_usage"]

        # save ram info
        obj.memory_total = memory['total']
        obj.memory_available = memory['available']
        obj.memory_used = memory['used']
        obj.memory_percentage = memory['percentage']

        # save swap info
        obj.swap_total = swap['total']
        obj.swap_free = swap['free']
        obj.swap_used = swap['used']
        obj.swap_percentage = swap['percentage']

        # save IO stats info
        obj.disk_read = iostats['disk_read']
        obj.disk_write = iostats['disk_write']
        obj.network_sent = iostats['network_sent']
        obj.network_received = iostats['network_received']
            
        obj.save()

        #delete old related tables
        Process.objects.filter(pc=obj).delete()
        Disk.objects.filter(pc=obj).delete()
        Cpu_Cores.objects.filter(pc=obj).delete()
        App.objects.filter(pc=obj).delete()
        
        # create list of running processes
        processes = json_data['processes']
        for item in processes:
            Process.objects.create(pc=obj, process_name=item['name'], process_id=item['pid'], process_start_time=item['start_time'], process_cpu_usage=item['cpu_usage'])
        
        # create list of partitions/disks
        disks = json_data['disks']
        for item in disks:
            Disk.objects.create(pc=obj, device=item['device'], mountpoint=item['mountpoint'], fstype=item['fstype'], total_size=item['total_size'], used=item['used'], free=item['free'], percentage=item['percentage'])
        
        # create list of cores
        cores = cpu['core_usage']
        for item in cores:    
            Cpu_Cores.objects.create(pc=obj, number=item['number'], usage=item['usage'])

        # create list of installed apps
        apps = json_data['list_of_apps']
        for item in apps:    
            App.objects.create(pc=obj, app=item)

        return HttpResponse('Data received')
    else:
        return HttpResponse('Invalid request method')
    