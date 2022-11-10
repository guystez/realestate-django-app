from django.urls import include, path
from . import views
 
app_name = 'property'
urlpatterns = [
   path('searchproperty/', views.searchproperty, name = "searchproperty" ),
   path('homepage/', views.home , name = "home"),
   path('result/', views.result , name = "result")
   
  
   

#    path('add/', views.add),
#    path('delete/', views.delete)
]


