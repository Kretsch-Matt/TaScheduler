import unittest
from django.test import RequestFactory
from django.contrib.auth.models import User

import scheduler.views
from scheduler.models import UserTable, CourseTable, UserCourseJoinTable, SectionTable, UserSectionJoinTable
from django.test import TestCase
from django.urls import reverse
from scheduler.views import InsCourseManagement


class TestAssignInstructorToSection(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = None

    def setUp(self):
        self.user1 = UserTable(firstName="adminTest", lastName="adminTest", email="adminTest@gmail.com",
                               phone="adminTest",
                               address="adminTest", userType="admin")
        self.user1.save()
        self.user1Account = User(username="adminTest", password="adpassword", email=self.user1.email)
        self.user1Account.save()

        self.user2 = UserTable(firstName="matt", lastName="matt", email="mattNew@gmail.com", phone="262-555-5555",
                               address="some address", userType="instructor")
        self.user2.save()
        self.user2Account = User(username="matt2", password="e121dfa91w", email=self.user2.email)
        self.user2Account.save()

        self.course1 = CourseTable(courseName="unitTest")
        self.course1.save()

        self.section1 = SectionTable(name="unitTestSection", courseId=self.course1)
        self.section1.save()

    def tearDown(self):
        # Clean up test data
        self.course1.delete()
        self.user1.delete()
        self.user1Account.delete()
        self.user2.delete()
        self.user2Account.delete()
        self.section1.delete()

    def test_insCourseManagement_Admin(self):
        # only instructors can view the instructor course management page, testing if Admin can
        request = RequestFactory().get(reverse('insCourseManagement'))  # Use reverse to get the URL
        request.user = self.user1Account
        response = InsCourseManagement.as_view()(request)

        # Check if the response status code is 302
        self.assertEqual(response.status_code, 302)

    def test_insCourseManagement_Instructor(self):
        request = RequestFactory().get(reverse('insCourseManagement'))  # Use reverse to get the URL
        request.user = self.user2Account

        response = InsCourseManagement.as_view()(request)

        # Check if the response status code Redirect
        self.assertEqual(response.status_code, 200)

    def test_adminCourseManagement_assignInstructor(self):
        data1 = {
            'courseSelect': self.course1.id,
            'courseBtn': 'Submit Course'
        }
        data2 = {
            'sectionSelect': self.section1.id,
            'instructorSelect': self.user2.id,
            'insToSectionBtn': 'Assign Instructor To Section'
        }
        request = RequestFactory().post(reverse('insCourseManagement'), data=data1)
        request.user = self.user1Account
        response = InsCourseManagement.as_view()(request)
        self.assertEqual(response.status_code, 200)

        request2 = RequestFactory().post(reverse('insCourseManagement'), data=data2)
        request2.user = self.user1Account
        response = InsCourseManagement.as_view()(request2)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(UserSectionJoinTable.objects.filter(userId=self.user2, sectionId=self.section1).exists())


if __name__ == '__main__':
    unittest.main()
