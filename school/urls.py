
from django.urls import path
from . import views

app_name = "school"



urlpatterns = [
    path("list/", views.SchoolListAPIView.as_view(), name="list_school"),
    path("<uuid:pk>/classroom/list/", views.ClassRoomListAPIView.as_view(), name="list_school_classroom"),   
]
