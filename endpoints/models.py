from django.db import models



class RSS_Feed_Keyowrds(models.Model):
    # id = models.AutoField(primary_key=True, auto_increment=False)
    id = models.IntegerField(primary_key=True)
    keywords =  models.TextField(unique=True)

    def __str__(self):
        return self.keywords
    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'



class RSS_Feed_Database(models.Model):
    # id = models.AutoField(primary_key=True, auto_increment=False)
    id = models.IntegerField(primary_key=True)
    feedName =  models.TextField()
    title = models.TextField(unique=True)
    publishedDate = models.DateTimeField()
    link = models.TextField()
    summary = models.TextField()

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class RSS_Feed_Name_Icon(models.Model):
    id = models.IntegerField(primary_key=True)
    feedName =  models.TextField(unique=True)
    feedIcon = models.TextField()
    feedFrequency_accepted = models.IntegerField(default = 0)
    feedFrequency_reject = models.IntegerField(default = 0)

    def __str__(self):
        return self.feedName
    class Meta:
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'

class RSS_Feed_URL(models.Model):
    id = models.IntegerField(primary_key=True)
    feedUrl = models.TextField(unique=True)

    def __str__(self):
        return self.feedUrl
    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'
        
        
class RSS_Feed_Temp(models.Model):
    id = models.IntegerField(primary_key=True)
    feedName =  models.TextField()
    title = models.TextField(unique=True)
    publishedDate = models.DateTimeField()
    link = models.TextField()
    summary = models.TextField()

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles(Discarded)'
# vikram sethi sir models
