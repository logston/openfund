import datetime

from yahoo_finance import Share as YFShare


def add_share(symbol):
    from .models import Share

    yfshare = YFShare(symbol)
    info = yfshare.get_info()

    if not info or len(info) == 1:
        raise ValueError('No share by the symbol {}'.format(symbol))

    company_name = info.get('CompanyName')
    symbol = info.get('symbol')
    start = info.get('start')
    end = info.get('end')

    if start:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()

    if end:
        end = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    kwargs = {
        'company_name': company_name,
        'symbol': symbol,
        'start': start,
        'end': end,
    }

    share = Share.objects.create(**kwargs)

    return share


def get_history_for_share(share, start=None, end=None):
    from .models import Quote

    if not start:
        start = share.start

    if not end:
        end = share.end

    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')

    yfshare = YFShare(share.symbol)
    history = yfshare.get_historical(start, end)

    for quote in history:
        quote = {k.lower(): v for k, v in quote.items()}
        date = quote.get('date')
        try:
            quote.pop('symbol')  # Don't need this
            quote['date'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            quote['share'] = share
            Quote.objects.create(**quote)
        except:
            print('Unable to create quote for {} / {}'.format(share, date))

