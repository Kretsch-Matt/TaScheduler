from django.contrib import admin
from .models import UserTable, CourseTable, LabTable, UserCourseJoinTable, SectionTable, CourseTA

# Register your models here.
admin.site.register(UserTable)
admin.site.register(CourseTable)
admin.site.register(LabTable)
admin.site.register(UserCourseJoinTable)
admin.site.register(SectionTable)
admin.site.register(CourseTA)
