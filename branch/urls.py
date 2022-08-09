from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('report/<str:number>/',views.report,name="report"),
    path('createreport/',views.createreport,name="createreport"),
    path('editreport/<str:number>/',views.editreport,name="editreport"),
    path('deletereport/<str:number>/',views.deletereport,name="deletereport"),
    path('loginuser/',views.loginuser,name="loginuser"),
    path('logoutuser/',views.logoutuser,name="logoutuser"),
    path('register/',views.register,name="register"),
    path('editcomment/<str:number>/',views.editcomment,name="editcomment"),
    path('deletecomment/<str:number>/',views.deletecomment,name="deletecomment"),
    path('profile/<str:number>/',views.profile,name="profile"),
    path('editprofile/<str:number>/',views.editprofile,name="editprofile"),
]