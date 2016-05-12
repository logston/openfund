import datetime

from yahoo_finance import Share as YFShare


def add_share(symbol):
    from .models import Share

    yfshare = YFShare(symbol)
    info = get_info_for_yfshare(yfshare)
    share = Share.objects.create(**info)

    return share


def get_info_for_yfshare(yfshare): 
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

    return kwargs


def get_history_for_share(share, start=None, end=None):
    from .models import Quote, Share
    
    yfshare = YFShare(share.symbol)
    info = get_info_for_yfshare(yfshare)
    share.start = info.get('start')
    share.end = info.get('end')
    share.save()
    
    if not start:
        start = share.start

    if not end:
        end = share.end

    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')

    history = yfshare.get_historical(start, end)

    quotes_by_date = {}
    for quote in history:
        quote = {k.lower(): v for k, v in quote.items()}
        date = quote.get('date')
        quote.pop('symbol')  # Don't need this
        quote['date'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        quote['share'] = share
        quotes_by_date[quote['date']] = Quote(**quote)

    # remove quotes that already exist in db
    dates = {q['date'] for q in share.quote_set.values('date')}
    for date in dates:
        del quotes_by_date[date]

    quotes = quotes_by_date.values()
    try:
        Quote.objects.bulk_create(quotes)
    except:
        count = len(quotes) 
        print('Unable to create {} quotes for {}'.format(count, share.symbol))

