from django.urls import path
from rest_framework.authtoken import views as authtoken_views


from . import views

urlpatterns = [
    path('login', authtoken_views.obtain_auth_token, name='api-get-token'),
    path('user/<int:pk>', views.user_profile, name='api-profile'),
    path('user/buddy_invites', views.UserBuddyInviteList.as_view(), name='api-user-buddy-invites'),
    path('user/buddies', views.UserBuddiesList.as_view(), name='api-user-buddies'),    
    path('user/parties', views.UserPartiesList.as_view(), name='api-user-parties'),
    path('send_invite', views.SendInvite.as_view(), name='api-send-invite'),
    path('cancel_invite', views.CancelInvite.as_view(), name='api-cancel-invite'),
    path('respond_to_invite', views.RespondToInvite.as_view(), name='api-respond-to-invite'),
    path('remove_buddy', views.RemoveBuddy.as_view(), name='api-remove-buddy'),
    path('buddy_invite/<int:pk>', views.BuddyInviteDetail.as_view(), name='api-buddy-invite'),
    path('movies/', views.movies, name='api-movies'),
    path('movies/<int:pk>', views.movie, name='api-movie'),
    path('shows/', views.shows, name='api-shows'),
    path('shows/<int:pk>', views.show, name='api-show'),
    path('shows/<int:pk>/seasons', views.season, name='api-show-seasons'),
    path('episodes/', views.episodes, name='api-episodes'),
    path('episodes/<int:pk>', views.episode, name='api-episode'),
    path('seasons/', views.seasons, name='api-seasons'),
    path('seasons/<int:pk>', views.season, name='api-season'),
    path('movies/<int:pk>/reviews', views.reviews, name='api-reviews'),
    path('movies/<int:pk>/review/<int:review_pk>', views.movie, name='api-review'),
    path('genres/', views.genres, name='api-genres'),
    path('genres/<int:pk>', views.genre, name='api-genre'),
    path('cast/', views.all_cast, name='api-all_cast'),
    path('cast/<int:pk>', views.cast, name='api-cast'),
    path('party/<int:pk>', views.PartyDetail.as_view(), name='api-party'),

]