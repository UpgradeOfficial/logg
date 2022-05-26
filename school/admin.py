from django.contrib import admin

# Register your models here.
from .models import Term,Expense,Fee,ClassRoom,Subject, Score,ClassRoomAttendance, QuestionAnswer, StudentAnswer

models = [
   Term,
   Expense,
   Fee,
   ClassRoom,
   Subject,
    Score,
    ClassRoomAttendance,
     QuestionAnswer,
      StudentAnswer
]
for model in models:
    admin.site.register(model)