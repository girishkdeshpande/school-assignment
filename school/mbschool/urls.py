from django.urls import path

from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('students', StudentViewSet, basename='students')
# router.register('courses', CourseViewSet, basename='courses')
# router.register('teachers', TeacherViewSet, basename='teachers')

urlpatterns = [
    path('students/', StudentList.as_view()),
    path('students/<int:pk>', StudentDetail.as_view()),
    path('students/<int:pk>', StudentCustom.as_view()),

    path('courses/', CourseList.as_view()),
    path('courses/<int:pk>', CourseDetail.as_view()),

    path('teachers/', TeacherList.as_view()),
    path('teachers/<int:pk>', TeacherDetail.as_view()),

]
