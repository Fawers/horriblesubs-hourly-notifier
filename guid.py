"""
Every item entry from HorribleSubs has a GUID. We're using it to keep track of what has already been broadcast
to the channel.
As of now, it'll be as simple as a single line file that contains the last show GUID.
"""

import os


FILEPATH = os.path.join(
    os.path.dirname(__file__),
    'guid.txt'
)


def read():
    try:
        with open(FILEPATH) as f:
            guid = f.read().strip()

    except FileNotFoundError:
        guid = ''
        write(guid)

    return guid


def write(guid):
    with open(FILEPATH, 'w') as f:
        return f.write(guid)
