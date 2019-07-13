import random
import os

from flask import current_app, g

# Generate a list of weighted customer ids
# Higher number means we are more likely to see that id
weighted_customer_ids = {
    '1f86decd': 20,
    'a71075f4': 30,
    '1250353a': 5,
    '4e9aaa78': 5,
    '1774f31b': 50,
    'aa4b5989': 10,
    'bfe93e1a': 15,
    'c2671b0d': 2,
    '72618136': 25,
    'fb553eb1': 10,
}
error_customers = set(['72618136', 'aa4b5989', 'bfe93e1a'])

# Turn the customer ids into a list where each id shows up as many times
# as defined in `weighted_customer_ids` e.g. `{'a': 3}`-> `['a', 'a', 'a']`
customer_ids = []
for customer_id, weight in weighted_customer_ids.items():
    customer_ids += [customer_id] * weight

# Shuffle the ids... why not
random.shuffle(customer_ids)


def get_customer_id():
    """Get a random customer id"""
    g.customer_id = random.choice(customer_ids)
    return g.customer_id


# Custom exception class
class CustomException(Exception):
    pass


def get_customer_data():
    current_app.logger.info('Fetching customer data')

    if os.environ.get('WORKSHOP_ADD_ERRORS') == 'true':
        customer_id = g.get('customer_id')
        if customer_id in error_customers:
            current_app.logger.warn(f'Fetching data for legacy customer {customer_id}')
            raise CustomException('An error has occurred')

    if 'customer_id' in g:
        return dict(customer_id=g.customer_id)
    return dict()


def get_request_headers():
    headers = dict()
    if hasattr(g, 'customer_id'):
        headers['x-customer-id'] = g.customer_id

    return headers
