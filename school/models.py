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
    school = models.ForeignKey('user.school', on_delete=models.CASCADE)
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
    students= models.ManyToManyField("user.Student")
    class_teacher = models.OneToOneField('user.Teacher', on_delete=models.PROTECT, null=True, blank=True)


class Subject(CoreModel):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey("school.ClassRoom", on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ManyToManyField('user.Teacher', blank=True, null=True)





class ClassRoomAttendance(CoreModel):
    students = models.ManyToManyField('user.student')
    classroom = models.ForeignKey('school.Classroom', on_delete=models.PROTECT)
    attendance_date = models.DateTimeField(auto_now_add=True)


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

class Announcement(CoreModel):
    school = models.ForeignKey("user.School", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.ForeignKey("school.ClassRoom", on_delete=models.SET_NULL, null=True, blank=True)
    

class Appointment(CoreModel):
    """
    Appointment model
    """
    class AppointmentStatus(models.TextChoices):
        BOOKED = "BOOKED", _("BOOKED")
        CANCELED = "CANCELLED", _("CANCELLED")
        CONFIRMED = "CONFIRM", _("CONFIRM")
        IN_PROGRESS = "IN_PROGRESS", _("IN_PROGRESS")
        COMPLETED = "COMPLETED", _("COMPLETED")
        
    initiator = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="initiator_appointment"
    )
    invitee = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="invitee_appointment"
    )
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.BOOKED)
    next_mail_schedule = models.DateField(null=True, blank=True)
# class Score(CoreModel):
#     subject = models.ForeignKey('school.Subject', on_delete=models.CASCADE)
#     student = models.ForeignKey('user.Student', on_delete=models.CASCADE)
#     score = models.DecimalField(decimal_places=2, max_digits=30)
#     total_score = models.DecimalField(decimal_places=2, max_digits=30)
# class QuestionAnswer(CoreModel):
#     question = models.ForeignKey("school.Question", on_delete=models.SET_NULL, null=True, blank=True)
#     index = models.CharField(max_length=50)
#     text = models.TextField()

# class StudentAnswer(CoreModel):
#     Qanswer = models.ForeignKey("school.QuestionAnswer", on_delete=models.SET_NULL, null=True, blank=True)
#     index = models.CharField(max_length=50)
#     text = models.TextField()
