from django.urls import path
from . import views

urlpatterns = [
        path('user/register/', views.postUser, name="postUser"), # POST
        path('user/login/', views.loginUser, name="loginUser"), # POST
        path('user/logout/', views.logoutUser, name="logoutUser"), # POST
        path('user/profile/', views.profileUser, name="profileUser"), # GET
        path('user/put/', views.putUser, name="putUser"), # PUT

        path('publication/all/', views.getPublications, name="getPublications"), # GET
        path('publication/register/', views.postPublicationDetail, name="postPublicationDetail"), # POST
        path('publication/put/<str:pk>', views.putPublicationDetail, name="putPublicationDetail"), # PUT
        path('publication/delete/<str:pk>', views.delPublicationDetail, name="delPublicationDetail"), # DELETE
        path('publication/user/<str:pk>', views.getPublicationUser, name="getPublicationUser"), # GET

        path('report/register/', views.postReportDetail, name="postReportDetail"), # POST
        ]
