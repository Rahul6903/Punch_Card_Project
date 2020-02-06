from django.urls import path
from . import views
urlpatterns=[
    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logout,name='logout'),
    path('logouts/',views.logouts,name='logouts'),

    path('employee/',views.employee,name='employee'),
    path('punch/', views.punch, name='punch'),
    path('detail/',views.detail,name='detail'),
    path('checkin/',views.checkin,name='check'),

    path('adminn/',views.adminn,name='adminn'),
    path('punch_admin/',views.punch_admin, name='punch_admin'),
    path('detail_admin/', views.detail_admin, name='detail_admin'),
    path('addemployee/',views.addemployee,name='addemployee'),
    path('next/',views.next,name='next'),
    path('previous/',views.previous,name='previous'),

]