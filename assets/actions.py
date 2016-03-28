import csv

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    filename = modeladmin.model._meta.verbose_name_plural + ".csv"
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    
    writer = csv.writer(response)
    writer.writerow(modeladmin.csv_fields)
    
    for line in queryset:
        row = []
        for field in modeladmin.csv_fields:
            attr = getattr(line, field)
            if hasattr(attr, 'pk'):
                attr = str(attr) + "(%s)" % attr.pk
            row.append(str(attr))
        writer.writerow(row)

    return response


def import_csv(obj, request):
    if not obj.has_add_permission(request):
        raise PermissionDenied
            
    opts = obj.model._meta
    model_title = opts.verbose_name_plural.title()
    
    if request.method == 'POST':
        file = request.FILES.get('input-file')
        if file.name.split('.')[-1] != 'csv':
            msg = 'Wrong file format. Please upload a CSV file.'
            obj.message_user(request, msg, level=messages.ERROR)
            return redirect("/admin/%s/%s/import/" % (opts.app_label, 
                                                      opts.model_name))

        _save_csv(obj, file)
        
        msg = 'Import success.'
        obj.message_user(request, msg, level=messages.INFO)

        return obj.response_post_save_add(request, None)
    else:
        data = {
            'title': 'Import %s from CSV' % model_title,
            'opts': opts,
            'app_label': opts.app_label,
            #'change': True,
            'has_file_field': True,
            #'has_add_permission': True,
            'has_change_permission': True,
        }
        return render_to_response('assets/import_form.html', data,
                                  context_instance=RequestContext(request))
        
def _save_csv(obj, csv_file):
    model = obj.model
    reader = csv.reader(csv_file)
    fields = reader.next()

    for row in reader:
        obj_dict = {}
        
        for i in range(len(fields)):
            field_value = row[i]
            #Create instance for foreign key fields
            if field_value == 'None':
                field_value = None
            elif fields[i] in dir(model):
                remote_model = getattr(model, fields[i]).field.remote_field.model
                if str(field_value).endswith(')'):
                    field_value = str(field_value).split('(')[-1][:-1]
                field_value = remote_model.objects.get(pk=field_value)
                
            obj_dict[fields[i]] = field_value

        obj = model(**obj_dict)
        obj.save()