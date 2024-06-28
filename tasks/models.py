from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum
from django.core.validators import MaxValueValidator, MinValueValidator

# class MyModel(models.Model):
#    username = models.CharField(max_length=100)
#    email = models.EmailField(max_length=254)
#    password = models.CharField(max_length=100)
#    confirm_password = models.CharField(max_length=100)
# class LikeDislikeManager(models.Manager):
#         use_for_related_fields = True

#         def likes(self):
#             # Забираем queryset с записями больше 0
#             return self.get_queryset().filter(vote__gt=0)

#         def dislikes(self):
#             # Забираем queryset с записями меньше 0
#             return self.get_queryset().filter(vote__lt=0)

#         def sum_rating(self):
#             # Забираем суммарный рейтинг
#             return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


# class LikeDislike(models.Model):
#    LIKE = 1
#    DISLIKE = -1

#    VOTES = ((DISLIKE, _('Не нравится')), (LIKE, _('Нравится')))

#    vote = models.SmallIntegerField(verbose_name=_("Голос"), choices=VOTES)
#    user = models.ForeignKey(User,
#                             verbose_name=_("Пользователь"),
#                             on_delete=models.CASCADE)

#    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#    object_id = models.PositiveIntegerField()
#    content_object = GenericForeignKey()
#    objects = LikeDislikeManager()


# class Article(models.Model):
#    votes = GenericRelation(LikeDislike, related_query_name='articles')

class LikeDislike(models.Model):
    LIKE = 1
# class Comment(models.Model):
#    votes = GenericRelation(LikeDislike, related_query_name='comments')
class Otzyv(models.Model):
    company = models.CharField(max_length=100, help_text="Название компании", unique=True)
    text = models.TextField(help_text="Текст отзыва", unique=True)
    Evaluation = models.IntegerField(help_text="Оценка",default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    plus = models.CharField(max_length=2000,help_text="Плюсы",default=" ")
    minus = models.CharField(max_length=2000,help_text="Минусы",default=" ")
    Image = models.ImageField(help_text="Картинка", default='tasks/static/images/Shaurum.png')
    def __str__(self):
        return "%s" % (self.company)
        
    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])


class Rating(models.Model):
    otzyv = models.ForeignKey(to=Otzyv, on_delete=models.CASCADE, help_text="Отзыв", related_name='ratings')
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField(verbose_name='Значение', choices=[(1, 'Нравится'), (-1, 'Не нравится')])
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')

    def __str__(self):
        return self.otzyv.company
