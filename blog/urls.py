from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tags/<str:tag_slug>', views.post_list, name='post_list_by_tag'),
    path('CBVpost_list/', views.Post_List.as_view(), name='CBVpost_list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/', views.post_details, name='post_details'),
    path('<int:id>/post_share/',views.post_share, name='post_share'),
    path('<int:id>/comment/',views.post_comment, name='post_comment'),
    path('post_search/',views.post_search, name='post_search'),
]