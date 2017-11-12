from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'loginPage$',(views.loginPage)),
    url(r'registration$', (views.registration)),
    url(r'register$',(views.register)),
    url(r'login$',(views.login))
]
