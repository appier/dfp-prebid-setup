import argparse
import logging

from tasks import add_new_prebid_partner
import settings

# Reference: http://prebid.org/prebid-mobile/adops-price-granularity.html
price_granularity_buckets = {

    'dense': [
        # min, max, increment
        (0, 2.99, 0.01),   # 0 - 3
        (3, 7.95, 0.05),   # 3 - 8
        (8, 19.50, 0.50),  # 8 - 20
        (20, 20, 0.0),  # cap at 20
    ]
}

price_multipliers = {
    'TWD': 30,
    'JPY': 110,
    'USD': 1
}


def main():
    settings.NO_CONFIRM = True

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bidders', required=False)
    parser.add_argument('-c', '--currency', required=False, default='USD')
    parser.add_argument('-g', '--granularity', required=False, default='dense')
    args = parser.parse_args()

    bidders = args.bidders.split(',') if args.bidders else [None]
    currency = args.currency
    granularity_type = args.granularity
    multiplier = price_multipliers[currency]

    # FIXME: it's bad to override globals like this, but due to the structure of the original code we have no choice.
    for bidder in bidders:
        settings.PREBID_BIDDER_CODE = bidder
        price_buckets = price_granularity_buckets[granularity_type]
        for (min_price, max_price, increment) in price_buckets:
            settings.PREBID_PRICE_BUCKETS = {
                'precision': 2,
                'min': min_price * multiplier,
                'max': max_price * multiplier,
                'increment': increment * multiplier,
            }

            logging.info('[Prebid Wrapper] Creating line items for: bidder: %s, currency: %s, granularity: %s',
                         bidder, currency, granularity_type)
            add_new_prebid_partner.main()


if __name__ == '__main__':
    main()
