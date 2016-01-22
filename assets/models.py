from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    resign = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    terminated_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class IPAddress(models.Model):
    STATUS_CHOICES = (
        ('IN_USE', 'In use'),
        ('ALLOCATED', 'Allocated'),
        ('FREE', 'Free'),
        ('UNKNOWN', 'Unknown')
    )
    ip_address = models.GenericIPAddressField(primary_key=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='UNKNOWN')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True)
    hostname = models.CharField(max_length=50, null=True, blank=True)
    mac_address = models.CharField(max_length=18, null=True, blank=True)
    
    def __str__(self):
        return self.ip_address
    
    
class Server(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('SHUTDOWN', 'Shutdown'),
        ('ERROR', 'Error'),
        ('UNKNOWN', 'Unknown')
    )
    server_id = models.CharField(max_length=50, primary_key=True)
    primary_ip = models.ForeignKey(IPAddress, null=True, blank=True)
    controll_ip = models.ForeignKey(IPAddress, related_name='ctl_servers')
    first_nic_mac = models.CharField(max_length=18)
    interface_port = models.CharField(max_length=32, null=True, blank=True)
    vlan_mode = models.CharField(max_length=32, null=True, blank=True)
    project = models.ForeignKey(Project,
                                on_delete=models.DO_NOTHING,
                                null=True,
                                blank=True)
    operation_system = models.CharField(max_length=10, null=True, blank=True)
    default_user = models.CharField(max_length=32, null=True, blank=True)
    default_password = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='UNKNOWN')
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return self.server_id


class Instance(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('SHUTDOWN', 'Shutdown'),
        ('ERROR', 'Error'),
        ('UNKNOWN', 'Unknown')
    )
    server_id = models.CharField(max_length=50, primary_key=True)
    primary_ip = models.ForeignKey(IPAddress)
    hostname = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    cluster = models.ForeignKey(Project,
                                on_delete=models.DO_NOTHING,
                                null=True,
                                blank=True)
    operation_system = models.CharField(max_length=10)
    state = models.CharField(max_length=10,
                             choices=STATUS_CHOICES,
                             default='UNKNOWN')
    default_user = models.CharField(max_length=32)
    default_password = models.CharField(max_length=32)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return self.server_id
