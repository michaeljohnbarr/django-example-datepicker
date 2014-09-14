from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from example.views import CreateTestModelView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'datepicker_example.views.home', name='home'),
    # url(r'^datepicker_example/', include('datepicker_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', view=CreateTestModelView.as_view(), name='example_home')
)
