from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("add-expense/", views.add_expense, name="add_expense"),
    path("delete-expense/<int:expense_id>/", views.delete_expense, name="delete_expense"),
    path("edit-expense/<int:expense_id>/", views.edit_expense, name="edit_expense"),
]