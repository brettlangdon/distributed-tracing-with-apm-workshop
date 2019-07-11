import random

from flask import g

# Generate a list of weighted user ids
# Higher number means we are more likely to see that id
weighted_user_ids = {
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
error_users = set(['72618136', 'a71075f4', 'bfe93e1a'])

# Turn the user ids into a list where each id shows up as many times
# as defined in `weighted_user_ids` e.g. `{'a': 3}`-> `['a', 'a', 'a']`
user_ids = []
for user_id, weight in weighted_user_ids.items():
    user_ids += [user_id] * weight

# Shuffle the ids... why not
random.shuffle(user_ids)


def get_user_id():
    """Get a random user id"""
    setattr(g, 'user_id', random.choice(user_ids))
    return g.user_id


# Custom exception class
class CustomException(Exception):
    pass


def maybe_raise_exception():
    if g.user_id in error_users:
        raise CustomException('An error has occurred')
