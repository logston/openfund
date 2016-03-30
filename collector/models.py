from django.db import models


class Share(models.Model):
    company_name = models.CharField(max_length=128)
    symbol = models.CharField(
        max_length=16,
        db_index=True,
    )
    start = models.DateField()
    end = models.DateField()
    industry = models.CharField(max_length=128)
    sector = models.CharField(max_length=128)


class Quote(models.Model):
    share = models.ForeignKey('collector.Share')
    date = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    adj_close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    volume = models.IntegerField()


