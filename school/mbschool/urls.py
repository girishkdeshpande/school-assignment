from django.urls import path, resolve

from rest_framework_simplejwt import views

from .views import *


urlpatterns = [
        # path('token/', views.TokenObtainPairView.as_view(), name='obtain-token'),
        # path('token/refresh/', views.TokenRefreshView.as_view(), name='refersh-token'),
        path('students/', StudentList.as_view(), name='students'),
        path('students/<int:pk>', StudentDetail.as_view(), name='student'),
        path('studentcourse/', StudentCustom.as_view(), name='studentcourse'),
        path('searchstudent/', SearchStudent.as_view(), name='searchstudent'),

        path('courses/', CourseList.as_view(), name='course'),
        path('courses/<int:pk>', CourseDetail.as_view(), name='courses/id'),
        path('searchcourse/', SearchCourse.as_view(), name='searchcourse'),

        path('teachers/', TeacherList.as_view(), name='teachers'),
        path('teachers/<int:pk>', TeacherDetail.as_view(), name='teacher'),
        path('teachercourse/', TeacherCustom.as_view(), name='teachercourse'),
        path('searchteacher/', SearchTeacher.as_view(), name='searchteacher'),

        path('users/', UserList.as_view(), name='users'),
        path('userlogin/', UserLogin.as_view(), name='user-login'),

    ]



