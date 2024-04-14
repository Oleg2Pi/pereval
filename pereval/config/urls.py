from django.contrib import admin
from django.urls import path
from data_of_pereval.views import PerevalCreateViewset, PerevalUpdateViewset, PerevalUserListViewset


urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitData/', PerevalCreateViewset.as_view({'post': 'create'})),
    path('submitData/<int:pk>/', PerevalUpdateViewset.as_view({'put': 'update', 'get': 'retrieve', 'delete':
        'destroy'})),
    path('submitData/user__email=<str:email>/', PerevalUserListViewset.as_view()),
]