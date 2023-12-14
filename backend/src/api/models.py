from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
  buddies = models.ManyToManyField("self", through="Buddies")
  groups = models.ManyToManyField("Group", through="GroupStatus",
                                    related_name="members")
  parties = models.ManyToManyField("WatchParty", through="PartyStatus",
                                    related_name="participants")
  media= models.ManyToManyField("Media", through="UserMediaInteraction", 
                                related_name="interactors")


class Group(models.Model):
    name = models.TextField()

    
class WatchParty(models.Model):
    datetime = models.DateTimeField()
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="parties")
    media = models.ForeignKey("Media", on_delete=models.CASCADE, related_name="parties")


class Media(models.Model):
    MOVIE = 1
    SHOW = 2
    EPISODE = 3

    TYPES = (
        (MOVIE, "MOVIE"),
        (SHOW, "SHOW"),
        (EPISODE, "EPISODE"),
    )

    title = models.TextField()
    media_type = models.PositiveSmallIntegerField(choices=TYPES)                                
    tv_show = models.ForeignKey("self", on_delete=models.CASCADE, blank=True,
                                null=True, related_name="episodes")
    next_media = models.OneToOneField("self", blank=True, null=True, 
                                      on_delete=models.CASCADE,
                                      related_name="previous_media")
    season = models.ForeignKey("season", blank=True, null=True, 
                               on_delete=models.CASCADE, 
                               related_name="episodes")
    episode_num = models.PositiveIntegerField(blank=True, null=True)
    
    crew = models.ManyToManyField("Cast", on_delete=models.CASCADE)  
    cover_image = models.ImageField(blank=True, null=True)

    @property
    def avg_rating(self):
        return round(UserMediaInteraction.objects.filter(media__pk=self.pk)\
    .aggregate(rating=models.Avg("rating",default=0))["rating"], 2)

    def __str__(self):
        return f"{self.title}"


class Season(models.Model):
    title = models.TextField()
    season_num = models.PositiveIntegerField()

    
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


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    visibility = models.IntegerField()


class Buddies(models.Model):
    PENDING = 0
    APPROVED = 1

    STATUSES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    buddy = models.ForeignKey("User", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUSES)

    class Meta:
        unique_together = ['user', 'buddy']


class GroupStatus(models.Model):
    PENDING = 0
    APPROVED = 1

    STATUSES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUSES)

    class Meta:
        unique_together = ['user', 'group']


class PartyStatus(models.Model):
    PENDING = 0
    APPROVED = 1

    STATUSES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    party = models.ForeignKey("WatchParty", on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUSES)

    class Meta:
        unique_together = ['user', 'party']


class UserMediaInteraction(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    media = models.ForeignKey("Media", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, blank=True,
                                null=True)
    rating = models.FloatField(blank=True, null=True,
                               choices=[(i/2,i/2) for i in range(11)])

    class Meta:
        unique_together = ['user', 'media', 'comment']