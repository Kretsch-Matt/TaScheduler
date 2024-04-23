import unittest
from unittest import TestCase
import django

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse

from adminAssignmentPage import AdminAssignmentPage
from scheduler.models import UserTable, CourseTable, LabTable
from scheduler.views import AdminAccManagement


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
        self.app.createCourse("Course1", self.user1.id)
        self.assertEqual(CourseTable.objects.filter(courseName="Course1").count(), 1)

    def test_createCourse_noInstructor(self):
        #returns true if invalid instructor ID
        with self.assertRaises(Exception):
            self.app.createCourse("Course10", 10)


class TestCreateAccount(unittest.TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()

    def test_createAccountSuccess(self):
        result = self.app.createAccount('user', 'testuser@example.com', 'password')
        self.assertIsNone(result)

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


class TestEditAccount(unittest.TestCase):
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


class TestDeleteAccount(unittest.TestCase):
    # FIXME this unit test needs some correcting
    def setUp(self):
        self.app = AdminAssignmentPage()
        #user 1
        self.user1 = UserTable(firstName="John", lastName="Doe", email="John@gmail.com", phone="262-724-8212",
                               address="some address", userType="Instructor")
        self.user1.save()
        self.user1Account = User(username="john", email=self.user1.email,  password="password123")
        self.user1Account.save()
        #user 2
        self.user2 = UserTable(firstName="Jeff", lastName="Doe", email="Jeff@gmail.com", phone="262-724-8212",
                               address="some address", userType="Instructor")
        self.user2.save()
        self.user2Account = User(username="jeff", email=self.user2.email, password="password123")
        self.user2Account.save()

    def test_deleteAccount(self):
        result = self.app.deleteAccount(self.user1Account.username, self.user1.email)
        self.assertEqual(True, result)

    def test_deleteAccountInvalidAccount(self):
        result = self.app.deleteAccount("Joe", "Joe@email.com")
        self.assertEqual(False, result)

    def test_deleteAccountEmptyArguments(self):
        result = self.app.deleteAccount("", "")
        self.assertEqual(False, result)

    def test_deleteAccountEmptyUsername(self):
        result = self.app.deleteAccount("", self.user1.email)
        self.assertEqual(False, result)

    def test_deleteAccountEmptyEmail(self):
        result = self.app.deleteAccount(self.user1Account.username, "")
        self.assertEqual(False, result)

    def test_deleteAccountWrongEmail(self):
        result = self.app.deleteAccount(self.user1Account.username, self.user2.email)
        self.assertEqual(False, result)

    def test_deleteTwoAccount(self):
        result = self.app.deleteAccount(self.user1Account.username, self.user1.email)
        result2 = self.app.deleteAccount(self.user2Account.username, self.user2.email)
        self.assertEqual(True, result, result2)

    def test_invalidArg(self):
        with self.assertRaises(TypeError):
            self.app.deleteAccount(1, self.user1.email)

    def test_deleteSameAccountTwice(self):
        result = self.app.deleteAccount(self.user1Account.username, self.user1.email)
        result2 = self.app.deleteAccount(self.user1Account.username, self.user1.email)
        self.assertEqual(False, result2)


class TestDeleteAccountACCEPTANCE(django.test.TestCase):
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
        requestCopy['deleteAccountName'] = 'deleteTest'
        requestCopy['deleteAccountEmail'] = 'deleteTest@gmail.com'
        requestCopy['deleteAccBtn'] = 'Delete'

        request.POST = requestCopy

        response = AdminAccManagement.as_view()(request)

        self.assertContains(response, 'Account deleted successfully')

    def test_adminAccManagement_DeleteNotExist(self):
        request = RequestFactory().post(reverse('adminAccManagement'))
        request.user = self.user1Account

        requestCopy = request.POST.copy()
        requestCopy['deleteAccountName'] = 'NoAcc'  # Provide username to delete
        requestCopy['deleteAccountEmail'] = 'notReal@gmail.com'  # Provide email to delete
        requestCopy['deleteAccBtn'] = 'Delete'  # Simulate button click

        request.POST = requestCopy

        response = AdminAccManagement.as_view()(request)

        self.assertContains(response, 'Failed to delete account')


if __name__ == '__main__':
    unittest.main()