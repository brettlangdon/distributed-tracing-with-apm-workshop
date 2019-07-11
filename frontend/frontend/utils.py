import random

# Generate a list of weighted user ids
# Higher number means we are more likely to see that id
weighted_user_ids = {
    '1f86decd': 20,
    'a71075f4': 20,
    '1250353a': 5,
    '4e9aaa78': 5,
    '1774f31b': 50,
    'aa4b5989': 10,
    'bfe93e1a': 15,
    'c2671b0d': 2,
    '72618136': 25,
    'fb553eb1': 10,
}

# Turn the user ids into a list where each id shows up as many times
# as defined in `weighted_user_ids` e.g. `{'a': 3}`-> `['a', 'a', 'a']`
user_ids = []
for user_id, weight in weighted_user_ids.items():
    user_ids += [user_id] * weight

# Shuffle the ids... why not
random.shuffle(user_ids)


def get_user_id():
    """Get a random user id"""
    return random.choice(user_ids)


# Custom exception class
class CustomException(Exception):
    pass


def maybe_raise_exception(rate=0.2):
    if random.random() < rate:
        raise CustomException('An error has occurred')
