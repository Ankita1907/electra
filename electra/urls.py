from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('<int:num>/', views.home, name='home'),
    path('', views.landing ,name='landing'),
     path('logout', views.logout_view ,name='logout_view'),
    path('tutorial', views.tutorial ,name='tutorial'),
    path('leaderboard/', views.leaderboard ,name='leaderboard'),
    path('start/', views.start ,name='start'),
    path('administrator/<int:num>/', views.administrator ,name='administrator'),
    path('comment/<int:st>/<int:num>/', views.comment ,name='comment'),
    path('questions/', views.questions, name='questions'),
    path('participant/', views.participant, name='participant'),
    path('auth/', include('social_django.urls', namespace='social')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)