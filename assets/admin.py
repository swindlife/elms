from django.contrib import admin
from django.conf.urls import url
from .actions import import_csv, export_csv

# Register your models here.

from .models import IPAddress, Server, Project, User


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'owner', 'project', 'hostname', 'status', )
    search_fields = ['ip_address', 'owner__id', 'project__name', 'status']
    csv_fields = ('ip_address', 'owner', 'project', 'hostname', 'status', 'mac_address')

    def get_urls(self):
        urls = super(IPAddressAdmin, self).get_urls()
        my_urls = [
            url(r'^import/$', self.admin_site.admin_view(self.import_csv),
                name="assets_ipaddress_import"),
        ]
        return my_urls + urls

    def import_csv(self, request):
        return import_csv(self, request)
            

class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_id', 'primary_ip', 'project', 'state')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'created_at')
    fields = ('name', 'description', 'owner', 'created_at')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    


admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(User, UserAdmin)

export_csv.short_description = "Export selected objects"
admin.site.add_action(export_csv)