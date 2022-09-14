from django.contrib import admin
from .models import Assignment, College, Files, courseTopic, course, grades, myAssignment, myFiles, mytopics, mycourses, courseUnit, myCourseUnit, profile, Announcement

# Register your models here.

admin.site.register(course)
admin.site.register(Announcement)
admin.site.register(courseTopic)
admin.site.register(courseUnit)
admin.site.register(Assignment)

admin.site.register(mycourses)
admin.site.register(mytopics)
admin.site.register(myCourseUnit)
admin.site.register(myAssignment)
admin.site.register(grades)
admin.site.register(College)
admin.site.register(Files)
admin.site.register(myFiles)

admin.site.register(profile)
