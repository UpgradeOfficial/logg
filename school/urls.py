
from django.urls import path
from . import views

app_name = "school"



urlpatterns = [
    path("list/", views.SchoolListAPIView.as_view(), name="list_school"),
    path("<uuid:pk>/classroom/list/", views.ClassRoomListAPIView.as_view(), name="list_school_classroom"),  
    path("classroom/", views.ClassRoomCreateAPIView.as_view(), name="create_classroom"), 
    path("subject/", views.SubjectCreateAPIView.as_view(), name="create_subject"),
    path("term/", views.TermCreateAPIView.as_view(), name="create_term"),
    path("expense/", views.ExpenseCreateAPIView.as_view(), name="create_expense"),
    path("fee/", views.FeeCreateAPIView.as_view(), name="create_fee"),
    path("classroom-attendance/", views.ClassRoomAttendanceCreateAPIView.as_view(), name="create_classroom_attendance"),
]
