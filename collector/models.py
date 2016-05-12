from django.db import models


class Share(models.Model):
    company_name = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    symbol = models.CharField(
        unique=True,
        max_length=16,
        db_index=True,
    )

    start = models.DateField(
        null=True,
        blank=True,
    )

    end = models.DateField(
        null=True,
        blank=True,
    )

    industry = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    sector = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.symbol


class Quote(models.Model):
    share = models.ForeignKey('collector.Share')

    date = models.DateField( 
        db_index=True,
    )

    open = models.FloatField(
        null=True,
        blank=True,
    )

    close = models.FloatField(
        null=True,
        blank=True,
    )

    adj_close = models.FloatField(
        null=True,
        blank=True,
    )

    low = models.FloatField(
        null=True,
        blank=True,
    )

    high = models.FloatField(
        null=True,
        blank=True,
    )

    volume = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('share', 'date')

    def __str__(self):
        return '{} / {}'.format(self.share.symbol, self.date)

