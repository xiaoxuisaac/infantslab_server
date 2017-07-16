from django.conf.urls import url, include
from django.views.generic.base import RedirectView
import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^generate/$', views.gen_email, name='gen_email'),
    url(r'^send/$', views.send_email, name='send_email'),
    url(r'^update_labels/$', views.update_labels, name='update_labels'),
    url(r'^update_template/$', views.update_content_from_template, name='update_content_from_template'),
    url(r'label_id/$', views.get_label_id, name='get_label_id'),
    url(r'add_template/$', views.add_template, name='add_template'),
    url(r'delete_old_templates/$', views.delete_old_templates, name='delete_old_templates'),
    url(r'^update_from_gmail/$', TemplateView.as_view(template_name="update.html"), name="update_from_gmail")
    
    ]