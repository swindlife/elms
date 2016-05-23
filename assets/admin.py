from django.contrib import admin
from django.conf.urls import url
from .actions import import_csv, export_csv

# Register your models here.

from .models import IPAddress, Server, Project, User


class ModelAdminWithImportView(admin.ModelAdmin):
    def get_urls(self):
        urls = super(ModelAdminWithImportView, self).get_urls()
        
        opts = self.model._meta
        my_urls = [
            url(r'^import/$', self.admin_site.admin_view(self.import_csv),
                name="assets_"+opts.model_name+"_import"),
        ]
        return my_urls + urls
    
    def import_csv(self, request):
        return import_csv(self, request)


class IPAddressAdmin(ModelAdminWithImportView):
    list_display = ('ip_address', 'owner', 'project', 'hostname', 'status', )
    search_fields = ['ip_address', 'owner__id', 'project__name', 'status']
    csv_fields = ('ip_address', 'owner', 'project',
                  'hostname', 'status', 'mac_address')


class ServerAdmin(ModelAdminWithImportView):
    list_display = ('server_id', 'primary_ip', 'project', 'state')
    csv_fields = ('server_id', 'primary_ip', 'controll_ip', 'first_nic_mac',
                  'interface_port', 'vlan_mode', 'operation_system', 
                  'default_user', 'default_password', 'state', 'comments')


class ProjectAdmin(ModelAdminWithImportView):
    list_display = ('name', 'description', 'owner', 'created_at')
    fields = ('name', 'description', 'owner', 'created_at')
    csv_fields = ('name', 'description', 'owner', 'created_at',
                  'terminated_at', 'deleted')


class UserAdmin(ModelAdminWithImportView):
    list_display = ('id', 'name', 'email')
    csv_fields = ('id', 'name', 'email', 'resign')


admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(User, UserAdmin)

export_csv.short_description = "Export selected objects"
admin.site.add_action(export_csv)