from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', (views.index)),
    url(r'^refineSearch$',(views.refineSearch)),
    url(r'^logout$',(views.logout)),
    url(r'^histSearch/(?P<id>\d*)$',(views.histSearch)),
    url(r'^instructions$',views.instructions)
]
