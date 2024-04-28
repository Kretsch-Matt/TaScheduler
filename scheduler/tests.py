import unittest

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

import scheduler.views
from adminAssignmentPage import AdminAssignmentPage
from scheduler.models import UserTable, CourseTable, LabTable
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from scheduler.views import AdminAccManagement


# Acceptance Tests for Login
class LoginTestCase(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(username='testuser', password='password')
        self.login_url = reverse('login')
        self.home_url = reverse('home')

    def test_login_success(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, expected_url=reverse('home'))

    def test_login_failure(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrong'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_redirect_to_home(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password'}, follow=True)
        self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        logout_url = reverse('logout')
        response = self.client.get(logout_url, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, expected_url=reverse('login'))


class TestCreateCourse(unittest.TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()
        self.user1 = UserTable(firstName="matt", lastName="matt", email="matt@gmail.com", phone="262-555-5555",
                               address="some address", userType="Instructor")
        self.user1.save()
        self.user1Account = User(username="matt", password="e121dfa91w", email=self.user1.email)
        self.user1Account.save()

    def tearDown(self):
        # Clean up test data
        self.user1.delete()
        self.user1Account.delete()

    def test_createCourse_correctly(self):
        self.app.createCourse("Course1", self.user1.id)
        course = CourseTable.objects.filter(courseName="Course1").first()

        self.assertEqual((course.courseName, course.instructorId.id), ("Course1", self.user1.id))

    def test_createCourse_duplicateName(self):
        self.app.createCourse("Course1", self.user1.id)
        with self.assertRaises(ValueError):
            self.app.createCourse("Course1", self.user1.id)
        self.assertEqual(CourseTable.objects.filter(courseName="Course1").count(), 1)

    def test_createCourse_noInstructor(self):
        #returns true if invalid instructor ID
        with self.assertRaises(ValueError):
            self.app.createCourse("Course10", 10)

    def test_createCourse_emptyCourseName(self):
        with self.assertRaises(ValueError):
            self.app.createCourse("", self.user1.id)


class TestCreateCourseAcc(TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()
        self.user1 = UserTable(firstName="adminTest", lastName="adminTest", email="adminTest@gmail.com", phone="adminTest",
                               address="adminTest", userType="admin")
        self.user1.save()
        self.user1Account = User(username="adminTest", password="adpassword", email=self.user1.email)
        self.user1Account.save()

        self.user2 = UserTable(firstName="deleteTest", lastName="deleteTest", email="deleteTest@gmail.com", phone="deleteTest",
                               address="deleteTest", userType="ta")
        self.user2.save()
        self.user2Account = User(username="deleteTest", password="delpassword", email=self.user2.email)
        self.user2Account.save()


        user2 = UserTable(firstName="Jeff", lastName="Thompson", email="nonadmin@gmail.com", phone="5484651456",
                         address="123 street", userType="instructor")
        user2.save()
        userAccount2 = User(username="JeffT", password="password123", email=user2.email)
        userAccount2.save()
    def tearDown(self):
        # Clean up test data
        self.user1.delete()
        self.user1Account.delete()
        self.user2.delete()
        self.user2Account.delete()

    def test_courseCourse_page(self):
        # Ensure that the course creation form is rendered correctly
        request = RequestFactory().get(reverse('courseManagement'))
        request.user = self.user1Account

        response = scheduler.views.courseManagement(request)


        self.assertEqual(response.status_code, 200)

    def test_courseManagement_redirect_non_admin(self):
        # Ensure that non-admin users are redirected to the home page when trying to access courseManagement
        request = RequestFactory().get(reverse('courseManagement'))
        request.user = self.user2Account

        response = scheduler.views.courseManagement(request)

        self.assertEqual(response.status_code, 302) #redirects

    def test_course_creation(self):
        # Create a test instructor
        instructor = UserTable.objects.create(firstName="John", lastName="Doe", email="john@example.com", phone="1234567890", address="123 Main St", userType="Instructor")
        self.client.login(username="adminTest", password="adpassword")
        # Ensure that a course can be created
        data = {
            'courseName': 'New Course',
            'instructorSelect': instructor.id,
            'createCourseBtn': 'Submit',  # button used
        }
        response = self.client.post(reverse('courseManagement'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CourseTable.objects.filter(courseName='New Course', instructorId=instructor).exists())

    def test_invalid_course_creation(self):
        # Ensure that an invalid course cannot be created
        data = {
            'courseName': '',  # Invalid empty course name
            'instructorSelect': 9999,  # Invalid instructor ID
        }
        response = self.client.post(reverse('courseManagement'), data)
        self.assertEqual(response.status_code, 302) #redirects to self
        self.assertFalse(CourseTable.objects.filter(courseName='', instructorId=9999).exists())


class TestCreateAccount(unittest.TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()

    def test_createAccountSuccess(self):
        result = self.app.createAccount('user', 'testuser@example.com', 'password')
        self.assertTrue(result)

    def test_createAccountEmptyUsername(self):
        with self.assertRaises(ValueError):
            self.app.createAccount('', 'testuser@example.com', 'password')

    def test_createAccountWithWeakPassword(self):
        with self.assertRaises(ValueError):
            self.app.createAccount('user', 'testuser@example.com', 'pass')

    def test_createAccountWithInvalidEmail(self):
        with self.assertRaises(ValueError):
            self.app.createAccount('user', 'not-an-email', 'password')

    def test_createAccountWithExistingUser(self):
        self.app.createAccount('user', 'testuser@example.com', 'password')
        with self.assertRaises(Exception) as context:
            self.app.createAccount('user', 'testuser@example.com', 'password')
            self.assertIn("User already exists", str(context.exception))


class CreateAccountTestCase(TestCase):
    def setUp(self):
        self.createAccount_url = reverse('createAccount')
        self.home_url = reverse('login')

    def tearDown(self):
        User.objects.filter(username='testuser', email='test@user.com').delete()
        UserTable.objects.filter(email='test@user.com').delete()

    def test_createAccount_success(self):
        response = self.client.post(self.createAccount_url,
                                    {'username': 'testuser', 'email': 'test@user.com', 'password': 'password'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser', email='test@user.com', password='password').exists())

    def test_createAccount_failure(self):
        with self.assertRaises(ValueError) as context:
            self.client.post(self.createAccount_url,
                             {'username': '', 'email': 'preExister@test.com', 'password': 'wordToPass'},
                             follow=True)
        self.assertEqual(str(context.exception), "Username cannot be empty")
        self.assertFalse(User.objects.filter(email='preExister@test.com').exists())


class TestEditAccount(TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()
        user = UserTable(firstName="John", lastName="Doe", email="email@gmail.com", phone="262-724-8212",
                         address="some address", userType="Instructor")
        user.save()
        userAccount = User(username="johnD", password="password123", userId=user.email)
        userAccount.save()

    def test_editAccount(self):
        newUser = self.app.editAccount(0, "newemail@uwm.com", "1234567890", "123 street", "TA")
        self.assertEqual(newUser,
                         UserTable(firstName="John", lastName="Doe", email="newemail@uwm.com", phone="1234567890",
                                   address="123 street", role="TA"))

    def test_editMissingAccount(self):
        self.assertRaises(ValueError,
                          self.app.editAccount(5, "newemail@uwm.com", "1234567890", "123 street", "TA"))


class TestDeleteAccount(TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()
        #user 1
        self.user1 = UserTable(firstName="John", lastName="Doe", email="John@gmail.com", phone="262-724-8212",
                               address="some address", userType="Instructor")
        self.user1.save()
        self.user1Account = User(username="john", email=self.user1.email, password="password123")
        self.user1Account.save()
        #user 2
        self.user2 = UserTable(firstName="Jeff", lastName="Doe", email="Jeff@gmail.com", phone="262-724-8212",
                               address="some address", userType="Instructor")
        self.user2.save()
        self.user2Account = User(username="jeff", email=self.user2.email, password="password123")
        self.user2Account.save()

    def test_deleteAccount(self):
        result = self.app.deleteAccount(self.user1Account.id, self.user1Account.id)
        self.assertEqual("Account deleted successfully", result)

    def test_deleteAccountInvalidAccount(self):
        result = self.app.deleteAccount(99999999, 99999999)
        self.assertEqual("Failed to delete account", result)

    def test_deleteAccountEmptyArguments(self):
        with self.assertRaises(ValueError):
            self.app.deleteAccount("", "")

    def test_deleteAccountEmptyUsername(self):
        with self.assertRaises(ValueError):
            self.app.deleteAccount("", self.user1.email)

    def test_deleteAccountEmptyEmail(self):
        with self.assertRaises(ValueError):
            self.app.deleteAccount(self.user1Account.username, "")

    def test_deleteAccountWrongEmail(self):
        result = self.app.deleteAccount(self.user1Account.id, self.user2Account.id)
        self.assertEqual("username/email match error", result)

    def test_deleteTwoAccount(self):
        result = self.app.deleteAccount(self.user1Account.id, self.user1Account.id)
        result2 = self.app.deleteAccount(self.user2Account.id, self.user2Account.id)
        self.assertEqual("Account deleted successfully", result, result2)

    def test_invalidArg(self):
        result = self.app.deleteAccount(1, "ID")
        self.assertEqual("username/email match error", result)

    def test_deleteSameAccountTwice(self):
        result = self.app.deleteAccount(self.user1Account.id, self.user1Account.id)
        result2 = self.app.deleteAccount(self.user1Account.id, self.user1Account.id)
        self.assertEqual("Failed to delete account", result2)

class TestDeleteAccountACCEPTANCE(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = None

    def setUp(self):
        self.app = AdminAssignmentPage()
        self.user1 = UserTable(firstName="adminTest", lastName="adminTest", email="adminTest@gmail.com", phone="adminTest",
                               address="adminTest", userType="admin")
        self.user1.save()
        self.user1Account = User(username="adminTest", password="adpassword", email=self.user1.email)
        self.user1Account.save()

        self.user2 = UserTable(firstName="deleteTest", lastName="deleteTest", email="deleteTest@gmail.com", phone="deleteTest",
                               address="deleteTest", userType="ta")
        self.user2.save()
        self.user2Account = User(username="deleteTest", password="delpassword", email=self.user2.email)
        self.user2Account.save()

    def tearDown(self):
        # Clean up test data
        self.user1.delete()
        self.user1Account.delete()
        self.user2.delete()
        self.user2Account.delete()

    def test_adminAccManagement_Admin(self):
        request = RequestFactory().get(reverse('adminAccManagement'))  # Use reverse to get the URL
        request.user = self.user1Account

        response = AdminAccManagement.as_view()(request)

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_adminAccManagement_Ta(self):
        request = RequestFactory().get(reverse('adminAccManagement'))  # Use reverse to get the URL
        request.user = self.user2Account

        response = AdminAccManagement.as_view()(request)

        # Check if the response status code Redirect
        self.assertEqual(response.status_code, 302)

    def test_adminAccManagement_DeleteAccount(self):
        request = RequestFactory().post(reverse('adminAccManagement'))
        request.user = self.user1Account

        requestCopy = request.POST.copy()
        requestCopy['deleteAccountName'] = self.user2.id
        requestCopy['deleteAccountEmail'] = self.user2.id
        requestCopy['deleteAccBtn'] = 'Delete'

        request.POST = requestCopy

        response = AdminAccManagement.as_view()(request)

        self.assertContains(response, 'Account deleted successfully')

    def test_adminAccManagement_DeleteNotExist(self):
        request = RequestFactory().post(reverse('adminAccManagement'))
        request.user = self.user1Account
        for userID in range(1, 9999):
            try:
                User.objects.get(id=userID)
            except User.DoesNotExist:
                requestCopy = request.POST.copy()
                requestCopy['deleteAccountName'] = userID  # Provide username to delete
                requestCopy['deleteAccountEmail'] = userID  # Provide email to delete
                requestCopy['deleteAccBtn'] = 'Delete'  # Simulate button click

                request.POST = requestCopy

                response = AdminAccManagement.as_view()(request)

                self.assertContains(response, 'Failed to delete account')

if __name__ == '__main__':
    unittest.main()
