import csv
from django.http import HttpResponse

from user.models import User

def download_csv(queryset):
    
    opts = queryset.model._meta
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=student_data.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

def create_student_user(first_name: str, last_name: str):
    first_name = first_name.lower()
    last_name = last_name.lower()
    email = f'{first_name}_{last_name}@logg_student.com' 
    password = f'{first_name}_{last_name}'
    user= User.objects.create_user(first_name=first_name, last_name=last_name, email=email, is_verified=True, password=password)
    return user