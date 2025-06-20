# ai_navigator/urls.py

from django.urls import path
from django.contrib import admin
from game import views as game_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', game_views.home, name='home'),
    path('dashboard/', game_views.dashboard, name='dashboard'),
    path('register/', game_views.user_register, name='user_register'),
    path('admin-register/', game_views.admin_register, name='admin_register'),
    path('login/', auth_views.LoginView.as_view(template_name='game/login.html'), name='login'),
    path('logout/', game_views.custom_logout, name='logout'),
    path('game/', game_views.game_view, name='game'),
    path('run_astar/', game_views.run_astar, name='run_astar'),
    path('run_dijkstra/', game_views.run_dijkstra, name='run_dijkstra'),
    path('show-db/', game_views.show_db, name='show_db'),
    path('export/', game_views.export_zip_csv, name='export_zip_csv'),
    path('user-activity-data/', game_views.user_activity_data, name='user_activity_data'),
    path('api/increment_games_played/', game_views.increment_games_played, name='increment_games_played'),
    path('api/clear_path_data/', game_views.clear_path_data, name='clear_path_data'),
]
