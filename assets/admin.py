from django.contrib import admin
from django.conf.urls import url
from django.core.exceptions import PermissionDenied, FieldError
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
            url(r'^import/$', self.admin_site.admin_view(self.import_csv),
                name="assets_ipaddress_import"),
        ]
        return my_urls + urls

    def import_csv(self, request):
        
        if not self.has_add_permission(request):
                raise PermissionDenied
            
        opts = self.model._meta
        model_title = opts.verbose_name_plural.title()
        
        if request.method == 'POST':
            file = request.FILES.get('input-file')
            if file.name.split('.')[-1] != 'csv':
                raise FieldError('Wrong file format. Please upload a CSV file.')
            self._save_csv(file)
            obj = None
            return self.response_post_save_add(request, obj)
        else:
            data = {
                'title': 'Import %s from CSV' % model_title,
                'opts': opts,
                'app_label': opts.app_label,
                'change': True,
                'has_file_field': True,
                'has_add_permission': True,
                'has_change_permission': True,
            }
            return render_to_response('assets/import_form.html', data,
                                      context_instance=RequestContext(request))
            
    def _save_csv(self, csv_file):
        pass


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