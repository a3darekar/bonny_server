from django.conf.urls import url, include

from .views import router
from .views import index, schedule_vaccines, generatePdf, UserListView, dataframe, prediction

urlpatterns = [
	url(r'^reports/', generatePdf, name='schedule_pdf'),
	url(r'api/schedule_vaccines/', schedule_vaccines),
	url(r'^dashboard/', dataframe),
	url(r'^prediction/', prediction),
	url(r'api/users/', UserListView.as_view()),
	url(r'^api/', include(router.urls)),
	url(r'^$', index),
]
