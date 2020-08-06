from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('test', views.test, name='test'),
    path('apriltag_project/', views.apriltag, name='apriltag'),
    path('clique_io_project/', views.cliqueio, name='cliqueio'),
    path('contact_me/', views.contact, name='contact'),
    path('submit/', views.save_contact_info, name='submit')
]
