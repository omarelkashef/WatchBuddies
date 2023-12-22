from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Q



from api.models import *
from .serializers import *


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs.get("pk"))

user_profile = UserDetail.as_view()


class SendBuddyInvite(APIView):  #can refacator into a genreal invite
    def post(self, request):
        curr_user_id = request.user.pk
        curr_user = User.objects.get(pk=curr_user_id)

        other_user_id = request.data.get('receiver_id')
        if curr_user_id == other_user_id:
            return Response({"error": "Can not send an invite to yourself"}, status=status.HTTP_404_NOT_FOUND)

        try:
            other_user = User.objects.get(pk=other_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if curr_user.buddies.filter(pk=other_user).exists():
            return Response({"error": "Users are already buddies"}, status=status.HTTP_400_BAD_REQUEST)
        
        invite, new = BuddiesInvite.objects.filter(
        Q(sender=curr_user, receiver=other_user) | Q(sender=other_user, receiver=curr_user)
    ).get_or_create(defaults={"sender": curr_user, "receiver": other_user})
        
        if new or (invite.responded and not invite.accepted):
            return Response({"message": "Buddy added successfully"}, status=status.HTTP_201_CREATED)

        return Response({"error": "The two users already have a valid invite"}, status=status.HTTP_400_BAD_REQUEST)


class CancelBuddyInvite(APIView):
    def post(self, request):
        sender_id = request.user.pk
        sender = User.objects.get(pk=sender_id)

        receiver_id = request.data.get('receiver_id')
        
        if sender_id == receiver_id:
            return Response({"error": "Can not send an invite to yourself"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if sender.buddies.filter(pk=receiver_id).exists():
            return Response({"error": "Users are already buddies"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            invite = BuddiesInvite.objects.filter(sender=sender, receiver=receiver).latest()
            if invite.responded:
                return Response({"error": "This invitation has already been accepted or declined"}, status=status.HTTP_400_BAD_REQUEST)
            invite.delete()
        except BuddiesInvite.DoesNotExist:
            return Response({"error": "This invitation does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Buddy deleted successfully"}, status=status.HTTP_201_CREATED)
    

class RespondToBuddyInvite(APIView):
    def post(self, request, accept):
        receiver_id = request.user.pk
        receiver = User.objects.get(pk=receiver_id)

        sender_id = request.data.get('sender_id')
        
        if sender_id == receiver_id:
            return Response({"error": "Can not send an invite to yourself"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            sender = User.objects.get(pk=sender_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            invite = BuddiesInvite.objects.get(sender=sender, receiver=receiver)
            invite.responded = True
            if accept:
                invite.accepted = True
                receiver.buddies.add(sender)
            invite.save()
        except BuddiesInvite.DoesNotExist:
            return Response({"error": "This invitation does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Buddy accepted successfully"}, status=status.HTTP_201_CREATED)
    

class MoviesList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

movies = MoviesList.as_view()


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

movie = MovieDetail.as_view()

class ShowsList(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

shows = ShowsList.as_view()


class ShowDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

show = ShowDetail.as_view()


class EpisodesList(generics.ListCreateAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

episodes = EpisodesList.as_view()


class EpisodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

episode = EpisodeDetail.as_view()


class SeasonsList(generics.ListCreateAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

seasons = SeasonsList.as_view()


class SeasonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

season = SeasonDetail.as_view()


class ShowSeasonsList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SeasonSerializer
    
    def get_queryset(self):
        return Season.objects.filter(show__pk=self.kwargs.get("show_pk"))


show_seasons = ShowSeasonsList.as_view()

class MediaReviewsList(generics.ListCreateAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        return Review.objects.filter(media__pk=self.kwargs.get("pk"))

reviews = MediaReviewsList.as_view()


class MediaReviewsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        return Review.objects.filter(pk=self.kwargs.get("review_pk"), 
                                    media__pk=self.kwargs.get("pk"))

review = MediaReviewsDetail.as_view()


class GenresList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

genres = GenresList.as_view()


class GenresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

genre = GenresDetail.as_view()


class CastList(generics.ListCreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer

all_cast = CastList.as_view()


class CastDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer

cast = CastDetail.as_view()


class PartiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchParty.objects.all()
    serializer_class = PartySerializer

party = PartiesDetail.as_view()