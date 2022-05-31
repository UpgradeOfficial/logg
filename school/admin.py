from django.contrib import admin

# Register your models here.
from .models import Term,Expense,Fee,ClassRoom,Subject, ClassRoomAttendance

models = [
   Term,
   Expense,
   Fee,
   ClassRoom,
   Subject,
    ClassRoomAttendance,
   
]
for model in models:
    admin.site.register(model)