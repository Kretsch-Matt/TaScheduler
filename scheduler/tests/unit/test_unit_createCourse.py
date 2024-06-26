import unittest
from unittest.mock import MagicMock, patch

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

import scheduler.views
from adminAssignmentPage import AdminAssignmentPage
from scheduler.models import UserTable, CourseTable, LabTable, UserCourseJoinTable, SectionTable, UserLabJoinTable, \
    UserSectionJoinTable
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from scheduler.views import AdminAccManagement


class TestCreateCourse(unittest.TestCase):
    def setUp(self):
        self.app = AdminAssignmentPage()
        self.user1 = UserTable(firstName="testinstructor", lastName="testinstructor", email="testinstructor@gmail.com", phone="262-555-5555",
                               address="some address", userType="instructor")
        self.user1.save()
        self.user1Account = User(username="testinstructor", password="testinstructor", email=self.user1.email)
        self.user1Account.save()

    def tearDown(self):
        # Clean up test data
        self.user1.delete()
        self.user1Account.delete()
        CourseTable.objects.filter(courseName="Course1").delete()

    def test_createCourse_correctly(self):
        self.app.createCourse("Course1", self.user1.id)
        course = CourseTable.objects.filter(courseName="Course1").first()

        self.assertEqual(course.courseName, "Course1")
        newJoin = UserCourseJoinTable.objects.filter(courseId=course).first()
        self.assertEqual(newJoin.userId, self.user1)
        course.delete()


    def test_createCourse_duplicateName(self):
        self.app.createCourse("Course1", self.user1.id)
        course = CourseTable.objects.filter(courseName="Course1").first()

        with self.assertRaises(ValueError):
            self.app.createCourse("Course1", self.user1.id)
        self.assertEqual(CourseTable.objects.filter(courseName="Course1").count(), 1)
        course.delete()

    def test_createCourse_noInstructor(self):
        # returns true if invalid instructor ID
        with self.assertRaises(ValueError):
            self.app.createCourse("Course10", 10)

    def test_createCourse_emptyCourseName(self):
        with self.assertRaises(ValueError):
            self.app.createCourse("", self.user1.id)


if __name__ == '__main__':
    unittest.main()
