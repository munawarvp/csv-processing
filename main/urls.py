
from django.urls import path

from main.views import UserDataView

urlpatterns = [
    path('user-data', UserDataView.as_view()),
]
