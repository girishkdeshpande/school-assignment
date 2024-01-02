from django.urls import path, include

from .views import StudentViewSet, CourseViewSet, TeacherViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students', StudentViewSet, basename='students')
router.register('courses', CourseViewSet, basename='courses')
router.register('teachers', TeacherViewSet, basename='teachers')

urlpatterns = [
    path('', include(router.urls))

]
