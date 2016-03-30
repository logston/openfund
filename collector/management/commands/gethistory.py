from django.core.management.base import BaseCommand, CommandError

from collector.models import Share
from collector.utils import get_history_for_share


class Command(BaseCommand):
    help = 'Get history for all shares'

    def add_arguments(self, parser):
        parser.add_argument('symbol')

    def handle(self, *args, **options):
        symbol = options['symbol']

        if symbol == 'allshares':
            shares = Share.objects.all()
        else:
            shares = Share.objects.filter(symbol=symbol)

        for share in shares:
            msg = 'Getting history for {}'.format(share)
            self.stdout.write(self.style.NOTICE(msg))
            get_history_for_share(share)

        self.stdout.write(self.style.SUCCESS('Done.'))

