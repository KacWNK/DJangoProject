from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('resetPassword', views.resetPassword, name='resetPassword'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerPage, name='register'),
    path('',views.home,name='home'),
    path('room/<str:prim>', views.room ,name='room'),
    path('create-challenge', views.createChallenge, name='create_challenge'),
    path('update_challenge/<str:prim>', views.updateChallenge, name='update_challenge'),
    path('delete_challenge/<str:prim>', views.deleteChallenge, name='delete_challenge'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)