from django.db import models

# Create your models here.

# main info
class Info(models.Model):
    # systeminfo
    system = models.CharField(max_length=200)
    node = models.CharField(max_length=200)
    relase = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    machine = models.CharField(max_length=200)
    processor = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField(null=True)
    mac_address = models.CharField(max_length=200)
    boot_time = models.DateTimeField(null=True, blank=True)

    # cpu
    physical_cores = models.PositiveIntegerField(null=True)
    total_cores = models.PositiveIntegerField(null=True)
    max_frequency = models.FloatField(null=True)
    min_frequency = models.FloatField(null=True)
    current_frequency = models.FloatField(null=True)
    core_usage = models.CharField(max_length=500)
    total_cpu_usage = models.FloatField(null=True)

    # memory
    memory_total = models.CharField(max_length=100)
    memory_available = models.CharField(max_length=100)
    memory_used = models.CharField(max_length=100)
    memory_percentage = models.FloatField(null=True)

    # swap
    swap_total = models.CharField(max_length=100)
    swap_free = models.CharField(max_length=100)
    swap_used = models.CharField(max_length=100)
    swap_percentage = models.FloatField(null=True)

    # IO stats
    disk_read = models.CharField(max_length=100)
    disk_write = models.CharField(max_length=100)
    network_sent = models.CharField(max_length=100)
    network_received = models.CharField(max_length=100)

    def __str__(self):
        return self.ip_address

# core info
class Cpu_Cores(models.Model):
    pc = models.ForeignKey(Info, on_delete=models.CASCADE)
    number = models.IntegerField(null=True)
    usage = models.FloatField(null=True)

# disk info
class Disk(models.Model):
    pc = models.ForeignKey(Info, on_delete=models.CASCADE)
    # disks
    device = models.CharField(max_length=100)
    mountpoint = models.CharField(max_length=100)
    fstype = models.CharField(max_length=100)
    total_size = models.CharField(max_length=100)
    used = models.CharField(max_length=100)
    free = models.CharField(max_length=100)
    percentage = models.FloatField(null=True)
    def __str__(self):
        return self.mountpoint

# running processes info
class Process(models.Model):
    pc = models.ForeignKey(Info, on_delete=models.CASCADE)
    # processes
    process_id = models.IntegerField(null=True)
    process_name = models.CharField(max_length=300)
    process_start_time = models.DateTimeField(null=True, blank=True)
    process_cpu_usage = models.FloatField(null=True)
    def __str__(self):
        return self.process_name

# installed apps info
class App(models.Model):
    pc = models.ForeignKey(Info, on_delete=models.CASCADE)
    app = models.CharField(max_length=500)