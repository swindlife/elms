from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse

# Register your models here.

from .models import IPAddress, Server, Project, User


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'owner', 'project', 'hostname', 'status', )
    search_fields = ['ip_address', 'owner__id', 'project__name', 'status']

    def get_urls(self):
        urls = super(IPAddressAdmin, self).get_urls()
        my_urls = [
            url(r'^my_view/$', self.my_view, name="assets_ipaddress_import"),
        ]
        return my_urls + urls

    def my_view(self, request):
		return HttpResponse("Import Data from CSV file.")


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