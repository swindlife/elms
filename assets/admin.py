from django.contrib import admin

# Register your models here.

from .models import IPAddress, Server, Project, User


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'owner', 'hostname', 'status')
    search_fields = ['ip_address', 'owner', 'hostname', 'status']


class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_id', 'primary_ip', 'project', 'state')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'descrption', 'owner', 'created_at')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    

admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(User, UserAdmin)