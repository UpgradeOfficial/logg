from django.db import models

from django.utils.translation import gettext_lazy as _

from core.models import CoreModel

# Create your models here.

class Term(CoreModel):
    class TERM_TYPE(models.TextChoices):
        '''
        '''
        FIRST = "FIRST", _("FIRST")
        SECOND = "SECOND", _("SECOND")
        THIRD = "THIRD", _("THIRD")
        
    name = models.CharField( _("name"),
        max_length=20,
        choices=TERM_TYPE.choices,
    )
    start_date = models.DateField()
    end_date = models.DateField()  


class Expense(CoreModel):
    term = models.ForeignKey(Term, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=30)

class Fee(CoreModel):
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    
class ClassRoom(CoreModel):
    name = models.CharField(max_length=100)
    school = models.ForeignKey("user.School", on_delete=models.CASCADE)
    class_teacher = models.OneToOneField('user.Teacher', on_delete=models.PROTECT, null=True, blank=True)


class Subject(CoreModel):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey("school.classroom", on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ManyToManyField('user.Teacher')



class Score(CoreModel):
    subject = models.ForeignKey('school.Subject', on_delete=models.CASCADE)
    student = models.ForeignKey('user.Student', on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, max_digits=30)
    total_score = models.DecimalField(decimal_places=2, max_digits=30)

class ClassRoomAttendance(CoreModel):
    student = models.ForeignKey('user.student', on_delete=models.PROTECT)
    classroom = models.ForeignKey('school.Classroom', on_delete=models.PROTECT)
    present = models.BooleanField(default=True)

class Question(CoreModel):
    class QUESTION_TYPE(models.TextChoices):
        SINGLE_ANSWER = "SINGLE_ANSWER", _("SINGLE_ANSWER")
        MULTI_CHOICE = "MULTI_CHOICE", _("MULTI_CHOICE")

    subject = models.ForeignKey("school.Subject", on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    question_type = models.CharField( _("question type"),
        max_length=20,
        choices=QUESTION_TYPE.choices,
    )
    answer = models.CharField(max_length=50)

class QuestionAnswer(CoreModel):
    question = models.ForeignKey("school.Question", on_delete=models.SET_NULL, null=True, blank=True)
    index = models.CharField(max_length=50)
    text = models.TextField()

class StudentAnswer(CoreModel):
    Qanswer = models.ForeignKey("school.QuestionAnswer", on_delete=models.SET_NULL, null=True, blank=True)
    index = models.CharField(max_length=50)
    text = models.TextField()
