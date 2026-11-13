from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.db.models import Sum, Count
from django.utils import timezone
from .forms import ExpenseForm

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "expenses/signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "expenses/login.html", {"form": form})

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")

    today = timezone.now().date()

    current_month = today.month
    current_year = today.year

    category = request.GET.get("category")

    if category:
        expenses = expenses.filter(category=category)

    expense_date = request.GET.get("date")

    if expense_date:
       expenses = expenses.filter(date=expense_date)   

    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0   

    total_expenses = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    expense_count = expenses.aggregate(
        count=Count("id")
    )["count"]

    highest_expense = expenses.order_by("-amount").first()

    category_summary = expenses.values("category").annotate(
        total=Sum("amount")
    ).order_by("-total")


    return render(
        request,
        "expenses/dashboard.html",
        {
            "expenses": expenses,
            "total_expenses": total_expenses,
            "expense_count": expense_count,
            "highest_expense": highest_expense,
            "category_summary": category_summary,
            "monthly_expenses": monthly_expenses,
        }
    )


@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            return redirect("dashboard")
    else:
        form = ExpenseForm()

    return render(request, "expenses/add_expense.html", {"form": form})

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("dashboard")

    return render(
        request,
        "expenses/delete_expense.html",
        {"expense": expense}
    )

@login_required
def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        "expenses/edit_expense.html",
        {"form": form, "expense": expense}
    )