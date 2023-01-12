from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login', views.loginShow),
    path('loginAuth', views.loginAuth),
    path('logout', views.logout),
    path('analysis', views.showAnalyze),
    path('graphData', views.getGraphData),
    path('districtStream', views.districtStreamCheck),

    path('view', views.showView),
    path('getDistrict', views.getDistrict),
    path('getDistrictData', views.getDistrictData),
    path('updateDistrictData', views.updateDistrictData),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'Server.views.errorPage'
