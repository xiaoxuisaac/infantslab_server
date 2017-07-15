from django.conf.urls import url, include
from django.views.generic.base import RedirectView
import views

urlpatterns = [
    url(r'^generate/$', views.gen_email, name='gen_email'),
    url(r'^send/$', views.send_email, name='send_email'),
    url(r'^update_label/$', views.update, name='update_label'),
    ]