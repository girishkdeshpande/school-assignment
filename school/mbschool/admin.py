from django.contrib import admin

from .models import Student, Course, Teacher

# admin.site.register(models.Student)
# admin.site.register(models.Course)


@admin.register(Student)
class StudentModel(admin.ModelAdmin):
    list_filter = ('student_name', 'student_status')
    list_display = ('student_name', 'student_status')


@admin.register(Course)
class CourseModel(admin.ModelAdmin):
    list_filter = ('course_name', 'course_status')
    list_display = ('course_name', 'course_status')


@admin.register(Teacher)
class TeacherModel(admin.ModelAdmin):
    list_filter = ('teacher_name', 'teacher_status')
    list_display = ('teacher_name', 'teacher_status')
