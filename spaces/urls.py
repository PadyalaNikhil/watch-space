from django.urls import path
from . import views_api, views_frontend

urlpatterns = [
    # Auth
    path('api/v1/auth/register', views_api.auth_register, name='auth_register'),
    path('api/v1/auth/signup/send-otp', views_api.auth_send_otp, name='auth_send_otp'),
    path('api/v1/auth/signup/verify-otp', views_api.auth_verify_otp, name='auth_verify_otp'),
    path('api/v1/auth/login', views_api.auth_login, name='auth_login'),
    path('api/v1/auth/logout', views_api.auth_logout, name='auth_logout'),
    path('api/v1/auth/me', views_api.auth_me, name='auth_me'),
    path('api/v1/auth/demo-users', views_api.auth_demo_users, name='auth_demo_users'),
    path('api/v1/auth/demo-switch', views_api.auth_demo_switch, name='auth_demo_switch'),

    # Titles & Timeline
    path('api/v1/titles', views_api.titles_list, name='titles_list'),
    path('api/v1/titles/import/netflix/search', views_api.netflix_search, name='netflix_search'),
    path('api/v1/titles/import/netflix/confirm', views_api.netflix_confirm_import, name='netflix_confirm_import'),
    path('api/v1/titles/<str:title_id>', views_api.title_detail, name='title_detail'),
    path('api/v1/titles/<str:title_id>/timeline', views_api.title_timeline, name='title_timeline'),
    path('api/v1/titles/<str:title_id>/timeline/validate', views_api.timeline_validate, name='timeline_validate'),
    path('api/v1/titles/<str:title_id>/timeline/publish', views_api.timeline_publish, name='timeline_publish'),

    # Watch Spaces (Rooms)
    path('api/v1/watch-spaces', views_api.watch_spaces_list_create, name='watch_spaces_list_create'),
    path('api/v1/watch-spaces/<str:room_id_or_code>', views_api.watch_space_detail, name='watch_space_detail'),
    path('api/v1/watch-spaces/<str:room_id_or_code>/join', views_api.watch_space_join, name='watch_space_join'),
    path('api/v1/watch-spaces/<str:room_id>/playback', views_api.watch_space_playback, name='watch_space_playback'),
    path('api/v1/watch-spaces/<str:room_id>/video/upload', views_api.watch_space_video_upload, name='watch_space_video_upload'),
    path('api/v1/watch-spaces/<str:room_id>/video/stream', views_api.watch_space_video_stream, name='watch_space_video_stream'),
    path('api/v1/watch-spaces/<str:room_id>/sync', views_api.watch_space_sync, name='watch_space_sync'),
    path('api/v1/watch-spaces/<str:room_id>/chat', views_api.watch_space_chat, name='watch_space_chat'),
    path('api/v1/watch-spaces/<str:room_id>/voice', views_api.watch_space_voice, name='watch_space_voice'),
    path('api/v1/watch-spaces/<str:room_id>/moderate', views_api.watch_space_moderate, name='watch_space_moderate'),
    path('api/v1/watch-spaces/<str:room_id>/end', views_api.watch_space_end, name='watch_space_end'),
    path('api/v1/watch-spaces/<str:room_id>/analytics', views_api.watch_space_analytics, name='watch_space_analytics'),

    # AI Content Engine
    path('api/v1/watch-spaces/<str:room_id>/ai/ask', views_api.ai_ask_copilot, name='ai_ask_copilot'),
    path('api/v1/watch-spaces/<str:room_id>/ai/context', views_api.ai_scene_context, name='ai_scene_context'),
    path('api/v1/watch-spaces/<str:room_id>/ai/trivia/trigger', views_api.ai_trivia_trigger, name='ai_trivia_trigger'),
    path('api/v1/watch-spaces/<str:room_id>/ai/variation/vote', views_api.ai_variation_vote, name='ai_variation_vote'),

    # Dashboard & Recommendations
    path('api/v1/dashboard', views_api.dashboard_data, name='dashboard_data'),
    path('api/v1/recommendations', views_api.recommendations_view, name='recommendations_view'),
    path('api/v1/recommendations/retrain', views_api.recommendations_retrain, name='recommendations_retrain'),

    # Frontend Single Page App views
    path('', views_frontend.index_view, name='frontend_index'),
    path('room/<str:room_id>', views_frontend.index_view, name='frontend_room'),
    path('room/<str:room_id>/', views_frontend.index_view),
    path('join/<str:invite_code>', views_frontend.index_view, name='frontend_join'),
    path('join/<str:invite_code>/', views_frontend.index_view),
    path('studio', views_frontend.index_view, name='frontend_studio'),
    path('studio/', views_frontend.index_view),
    path('auth', views_frontend.index_view, name='frontend_auth'),
    path('auth/', views_frontend.index_view),
    path('summary/<str:room_id>', views_frontend.index_view, name='frontend_summary'),
    path('summary/<str:room_id>/', views_frontend.index_view),
]
