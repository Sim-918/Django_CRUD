from django.urls import path
import myapp.views as mv

urlpatterns = [
    path('',mv.index),
    path('read/<id>/',mv.read),
    path('update/<id>/',mv.update),
    path('create/',mv.create),
    path('delete/',mv.delete)
]
