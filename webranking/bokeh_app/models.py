from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

from django.conf import settings
import django.db.models.deletion

class UserInfo(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)

    # adding information about the user that is not included in the model
    # BASICALLY OneToOneField means that
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    def __str__(self):
        return self.last_name
    #additional
    # block=True means that user doesn't need to provide their info
class WebInfo(models.Model):
    website = models.URLField(max_length=256, primary_key=True)
    userinfo = models.ForeignKey(UserInfo, null=True, related_name='websites', on_delete=models.PROTECT)
    # created_date = models.ForeignKey(default=datetime.datetime.now(), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL) #, primary_key=True,
    # created_date = models.DateTimeField(blank=True, null=True)

    #creating the exact Date
    # def created_date(self):
    #     self.created_date = timezone.now()
    #     salf.save()
    #
    # def get_absolute_ur(self):
    #     return reverse('index', kwargs={'pk':self.pk})
    # return the represention of the model object
    # returning the website name instated of the username
    def __str__(self):
        return self.website