from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from collector.models import Share
from collector.utils import get_history_for_share


class Command(BaseCommand):
    help = 'Get history for all shares'

    def add_arguments(self, parser):
        parser.add_argument('symbol')

    def handle(self, *args, **options):
        now = timezone.now()
        msg = 'Starting job at {}'.format(now)
        self.stdout.write(self.style.NOTICE(msg))
        self.stdout.flush()

        symbol = options['symbol']

        if symbol == 'allshares':
            shares = Share.objects.all()
        else:
            shares = Share.objects.filter(symbol=symbol)

        for share in shares.iterator():
            msg = 'Getting history for {}'.format(share)
            self.stdout.write(self.style.NOTICE(msg))
            self.stdout.flush()
            try:
                get_history_for_share(share)
            except KeyboardInterrupt:
                break
            except:
                msg = 'Unable to get history for {}'.format(share)
                self.stdout.write(self.style.NOTICE(msg))
                self.stdout.flush()

        now = timezone.now()
        self.stdout.write(self.style.SUCCESS('Done at {}.'.format(now)))
        self.stdout.flush()

