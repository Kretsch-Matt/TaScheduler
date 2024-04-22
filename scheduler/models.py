from django.contrib.auth.models import AbstractUser, User
from django.db import models


class AccountTable(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)


# Create your models here.
class UserTable(models.Model):
    # Fields
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255)
    userType = models.CharField(max_length=20)


class CourseTable(models.Model):
    # Fields
    courseName = models.CharField(max_length=30, unique=True)

    # Relationship Fields
    instructorId = models.ForeignKey(
        UserTable,
        on_delete=models.CASCADE,
    )


class LabTable(models.Model):
    # Fields
    sectionNumber = models.CharField(max_length=30)

    # Relationship Fields
    courseId = models.ForeignKey(
        CourseTable,
        on_delete=models.CASCADE,
    )
    taId = models.ForeignKey(
        UserTable,
        on_delete=models.CASCADE,
    )
