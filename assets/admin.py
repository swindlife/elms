from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import ImportCSVForm

# Register your models here.

from .models import IPAddress, Server, Project, User


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'owner', 'project', 'hostname', 'status', )
    search_fields = ['ip_address', 'owner__id', 'project__name', 'status']

    def get_urls(self):
        urls = super(IPAddressAdmin, self).get_urls()
        my_urls = [
            url(r'^import/$', self.import_csv, name="assets_ipaddress_import"),
        ]
        return my_urls + urls

    def import_csv(self, request):
        model_title = self.model._meta.verbose_name_plural.title()
        form = ImportCSVForm(request.POST, request.FILES)
        print request.FILES
        data = {
            'title': 'Import %s from CSV' % model_title,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'change': True,
            'has_file_field': True,
            'has_add_permission': True,
            'has_change_permission': True,
            #'adminform': form
        }
        return render_to_response('assets/import_form.html', data,
                                  context_instance=RequestContext(request))


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