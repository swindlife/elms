from django.contrib import admin

# Register your models here.

from .models import IPAddress, Server, Project, User


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'owner', 'project', 'hostname', 'status', )
    search_fields = ['ip_address', 'owner__id', 'project__name', 'status']


class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_id', 'primary_ip', 'project', 'state')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'created_at')
    fields = ('name', 'description', 'owner', 'created_at')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    

def export(modeladmin, request, queryset):
    pass
export.short_description = "Export selected objects"

admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(User, UserAdmin)

admin.site.add_action(export)