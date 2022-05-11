
from django.urls import path
from . import views

app_name = "user"



urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("initiate_password_reset", views.InitiatePasswordResetView.as_view(), name="password_reset"),
    path("change_password", views.ChangePasswordView.as_view(), name="change_password"),
    path("reset_password/<uuid:token>/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("confirm_email/<uuid:token>/", views.ConfirmEmailView.as_view(), name="confirm_email"),
]
