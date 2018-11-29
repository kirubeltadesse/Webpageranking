from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

from django.conf import settings
import django.db.models.deletion


class WebInfo(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    website = models.URLField(max_length=256, primary_key=True) #, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    # userinfo = models.ForeignKey(UserInfo, null=True, related_name='websites', on_delete=models.PROTECT)
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

class ParaInfo(models.Model):
    # created_date = models.DateTimeField(auto_now_add=True,null=True)
    web_address = models.URLField(max_length=256)
    load_time = models.CharField(max_length=50)
    first_byte = models.CharField(max_length=50)
    start_render = models.CharField(max_length=50)
    speed_Index = models.CharField(max_length=50)
    dom_elements = models.CharField(max_length=50)

    doc_complete_Requests = models.CharField(max_length=50)
    doc_complete_Byets = models.CharField(max_length=50)

    fully_time = models.CharField(max_length=50)
    fully_requests = models.CharField(max_length=50)
    fully_bytes = models.CharField(max_length=50)
    webinfo = models.ForeignKey(WebInfo, null=True, related_name='websites', on_delete=models.CASCADE)

    def __str__(self):
        return self.web_address

        # Waterfall view= result.data.runs[1].firstView.images.waterfall)
