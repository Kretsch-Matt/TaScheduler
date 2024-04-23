from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from pip._vendor.requests.models import Response

import adminAssignmentPage
from .models import CourseTable, UserTable, LabTable


def home(request):
    return render(request, 'home.html')


def courseManagement(request):
    courses = CourseTable.objects.all()
    TAs = UserTable.objects.filter(userType="TA")
    instructors = UserTable.objects.filter(userType="Instructor")
    labs = LabTable.objects.all()

    if request.method == 'GET':
        user = request.user
        accRole = UserTable.objects.get(email=request.user.email).userType
        if user.is_authenticated and accRole == 'admin':
            return render(request, 'courseManagement.html',
                          {'courses': courses, 'TAs': TAs, 'instructors': instructors, 'labs': labs})
        else:
            # Redirect non-admin users to another page (e.g., home page)
            return redirect('home')

    else:
        if request.method == 'POST':
            courseName = request.POST.get('courseName')
            courseTime = request.POST.get('courseTime')
            courseDays = request.POST.get('courseDays')
            instructor = request.POST.get('instructorSelect')

            # Create a new CourseTable object
            admin_page = adminAssignmentPage.AdminAssignmentPage()
            try:
                admin_page.createCourse(courseName, instructor)
                return render(request, 'courseManagement.html', {'courses': courses, 'TAs': TAs, 'instructors': instructors, 'labs': labs, 'messages': "Course successfully created"})
            except ValueError as msg:
                return render(request, 'courseManagement.html', {'courses': courses, 'TAs': TAs, 'instructors': instructors, 'labs': labs, 'messages': msg})
        return redirect('courseManagement')
    return render(request, 'courseManagement.html')


def createAccount(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        adminPage = adminAssignmentPage.AdminAssignmentPage()
        accountCreated = adminPage.createAccount(username=username, email=email, password=password)
        if accountCreated:
            return render(request, 'createAccount.html', {'username': username, 'email': email, 'password': password, 'messages': "Account created successfully"})
        else:
            return render(request, 'createAccount.html', {'username': username, 'email': email, 'password': password, 'messages': "Account failed to be created"})

    return render(request, 'createAccount.html')


class AdminAccManagement(View):
    @staticmethod
    def get(request):

        user = request.user
        accRole = UserTable.objects.get(email=request.user.email).userType
        if user.is_authenticated and accRole == 'admin':
            return render(request, 'adminAccManagement.html')
        else:

            # Redirect non-admin users to another page (e.g., home page)
            return redirect('home')

    @staticmethod
    def post(request):
        if request.method == 'POST':
            if 'deleteAccBtn' in request.POST:
                username = request.POST.get('deleteAccountName')
                email = request.POST.get('deleteAccountEmail')

                adminPage = adminAssignmentPage.AdminAssignmentPage()
                accDeleted = adminPage.deleteAccount(username=username, email=email)
                if accDeleted:
                    return render(request, 'adminAccManagement.html', {'message': "Account deleted successfully"})
                else:
                    return render(request, 'adminAccManagement.html', {'message': "Failed to delete account"})
            if 'createAccBtn' in request.POST:
                username = request.POST.get('createAccountName')
                email = request.POST.get('createAccountEmail')
                password = request.POST.get('createAccountPassword')
                adminPage = adminAssignmentPage.AdminAssignmentPage()
                accCreated = adminPage.createAccount(username=username, email=email, password=password)
                if accCreated:
                    return render(request, 'adminAccManagement.html', {'messageCreateAcc': "Account created"})
                else:
                    return render(request, 'adminAccManagement.html', {'messageCreateAcc': "Failed to create account"})
