from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('addbook', views.addbook),
    path('newbook', views.newbook),
    path('user/<int:id>', views.user),
    path('book/<int:id>', views.book),
    path('book/addreview', views.addreview),
    path('book/deletereview', views.deletereview)
]
