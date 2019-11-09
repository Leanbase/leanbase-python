import random

def random_emails(count):
    seed = int(random.random() * 10e12)
    return [
        'some{}email@domain.com'.format(a)
        for a in range(seed, seed + count)
    ]
