from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .api import PointViewSet, RouteViewSet
from rest_framework_nested import routers


app_name = "roads"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('scrap', views.scrap_page, name='scrap'),
    path('select_background/', views.select_background, name='select_background'),
    path('routes/create/', views.create_route, name='create_route'),
    path('create_board/', views.create_game, name='create_game'),
    path('background/', views.background, name='background'),
    path('routes/<int:route_id>/', views.route_detail, name='route_detail'),
    path('boards/<int:board_id>/', views.game_detail, name='game_detail'),
    path('points/delete/<int:pt_id>/', views.delete_point, name='delete_point'),
    path('boards/<int:board_id>/save/', views.save_board, name='save_board'),
    path('delete_board/<int:board_id>', views.delete_board, name='delete_board'),
    path('play/<int:board_id>', views.game_play, name='game_play'),
    path('boards/<int:board_id>/save_path/', views.save_path,   name='save_path'),
    path('delete_route/<int:route_id>', views.delete_route, name='delete_route'),
    path('sse/notifications/', views.sse_notifications, name='sse_notifications')
]

router = routers.SimpleRouter()
router.register(r'trasy', RouteViewSet, basename='trasy')

routes_router = routers.NestedSimpleRouter(router, r'trasy', lookup='route')
routes_router.register(r'punkty', PointViewSet, basename='route-punkty')

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/', include(routes_router.urls)),
]