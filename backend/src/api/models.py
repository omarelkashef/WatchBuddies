from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
  buddies = models.ManyToManyField("self")
  groups = models.ManyToManyField("Group", related_name="members")
  parties = models.ManyToManyField("WatchParty", related_name="members")
  media = models.ManyToManyField("Media", through="UserMediaInteraction", 
                                related_name="interactors")


class Group(models.Model):
    name = models.TextField()

    
class WatchParty(models.Model):
    datetime = models.DateTimeField()
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="parties")
    media = models.ForeignKey("Media", on_delete=models.CASCADE, related_name="parties")


class Cast(models.Model):
    ACTOR = 1
    DIRECTOR = 2
    CREW_MEMBERS = 3

    TYPES = (
        (ACTOR, "actor"),
        (DIRECTOR, "director"),
        (CREW_MEMBERS, "crew"),
    )

    first_name = models.TextField()
    last_name = models.TextField()
    cast_type = models.PositiveSmallIntegerField(choices=TYPES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=127)
    description = models.CharField(max_length=255)


class Media(models.Model):
    title = models.TextField() 
    release_date = models.DateField()
    
    next_media = models.OneToOneField("self", blank=True, null=True, 
                                      on_delete=models.CASCADE,
                                      related_name="previous_media")
    crew = models.ManyToManyField(Cast)  
    cover_image = models.TextField(default="static/images/no_cover_image.png")

    @property
    def avg_rating(self):
        return round(Review.objects.filter(media__pk=self.pk)\
    .aggregate(rating=models.Avg("rating", default=0))["rating"], 2)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        unique_together = ["title", "release_date"]


class Movie(Media):
    duration = models.DurationField()
    genre = models.ManyToManyField(Genre, blank=True, null=True,
                                   related_name="movies")


class Episode(Media):
    duration = models.DurationField()
    genre = models.ManyToManyField(Genre, blank=True, null=True,
                                   related_name="episodes")
    tv_show = models.ForeignKey("show", on_delete=models.CASCADE, blank=True,
                                null=True, related_name="episodes")
    season = models.ForeignKey("season", blank=True, null=True, 
                               on_delete=models.CASCADE, 
                               related_name="episodes")
    episode_num = models.PositiveIntegerField(blank=True, null=True)


class Show(Media):
    genre = models.ManyToManyField(Genre, blank=True, null=True, 
                                   related_name="shows")
    @property
    def num_season(self):
        # TODO
        return
    
    @property
    def num_episodes(self):
        # TODO
        return
    

class Season(models.Model):
    title = models.TextField()
    show = models.ForeignKey("show", on_delete=models.CASCADE)
    season_num = models.PositiveIntegerField(default=1)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    edited = models.BooleanField(default=False)
    rating = models.FloatField(blank=True, null=True,
                               choices=[(i/2,i/2) for i in range(11)])


class Invite(models.Model):
    first_sent = models.DateTimeField(auto_now_add=True)
    last_renewed = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class BuddiesInvite(Invite):
    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="send_buddies_invite")
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="received_buddies_invite")
    class Meta:
        unique_together = ['sender', 'receiver']


class GroupInvite(Invite):
    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="send_group_invite")
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="received_group_invite")
    group = models.ForeignKey("Group", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['receiver', 'group']

class PartyInvite(Invite):
    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="send_party_invite")
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="received_party_invite")
    party = models.ForeignKey("WatchParty", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['receiver', 'party']


class UserMediaInteraction(models.Model):
    WATCHED = 1
    FAVORITED = 2
    REVIEWED = 3
    LISTED = 4
    
    INTERACTION_TYPE = (
        (WATCHED, "watched"),
        (FAVORITED, "favorited"),
        (REVIEWED, "reviewed"),
        (LISTED, "listed")
    )

    ONLY_ME = -2
    MY_GROUPS = -1
    EVERYONE = 0

    user = models.ForeignKey("user", on_delete=models.CASCADE)
    media = models.ForeignKey("media", on_delete=models.CASCADE)
    interaction_type = models.PositiveSmallIntegerField(choices=INTERACTION_TYPE)
    review = models.OneToOneField("review", on_delete=models.CASCADE, null=True,
                                  blank=True)
    visibility = models.IntegerField()

    class Meta:
        unique_together = ["user", "media", "interaction_type"]
    
