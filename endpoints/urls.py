from django.urls import path
from . import views


urlpatterns = [
    path('',views.getRoutes),
    path('404/', views.custom_404_view),

    path('chat/chat',views.generate_response),
    path('chat/chat/',views.generate_response),
    
    path('keywords',views.getKeywordsAll),
    path('keywords/',views.getKeywordsAll),

    path('database',views.getDatabaseAll),
    path('database/',views.getDatabaseAll),

    path('nameicon',views.getNameIconAll),
    path('nameicon/',views.getNameIconAll),
    
    path('<str:feedname>/', views.getFeedArticles),
    path('<str:feedname>', views.getFeedArticles),    
    
    path('accept/<str:title>/', views.accept_article),
    path('accept/<str:title>', views.accept_article),
    
    path('reject/reject/', views.reject_article),
    path('reject/reject', views.reject_article),

]